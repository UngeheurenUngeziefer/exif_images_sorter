import os
from glob import glob
import exifread
import shutil
import logging as log
import time
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
start_time = time.time()


with open("pathes.yaml", "r") as yaml_file:
    pathes = list(yaml.load_all(yaml_file, Loader=SafeLoader))
    PATH_UNSORTED = pathes[0].get("PATH_UNSORTED").replace("/", "//")
    PATH_SORTED = pathes[0].get("PATH_SORTED").replace("/", "//")
    PATH_SORTED_READABLE = PATH_SORTED.replace("//", "/")
    PATH_UNSORTED_READABLE = PATH_UNSORTED.replace("//", "/")

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
date_time = str(datetime.now().strftime("%Y-%b-%d, %Hh %Mm"))
log.basicConfig(format="%(asctime)s - %(message)s", 
                datefmt="%d-%b-%y %H:%M:%S",
                handlers=[
                    log.FileHandler(f"{BASE_DIR}/logs/sorter_{date_time}.log"),
                    log.StreamHandler()
                    ])


# list of all .jpg files inside folder recursively
all_images_list = [y for x in os.walk(PATH_UNSORTED) 
                  for y in glob(os.path.join(x[0], '*.jpg'))]

log.warning(f"Found {len(all_images_list)} images overall!")

count_sorted_with_none = 0
count_sorted_with_date = 0
count_duplicates_stuck = 0

for image in all_images_list:
    image_name = image[(image.rfind("\\"))+1:]
    with open(image, 'rb') as image_file:
        tags = exifread.process_file(image_file)
                
        # we dont have EXIF date info 
        if "EXIF DateTimeOriginal" not in tags.keys():
            year = "None"
            month = "None"

        # we have EXIF date info
        else:
            for tag in tags.keys():
                if tag == "EXIF DateTimeOriginal":
                    exif_datetime_original = tags[tag]
                    year = str(exif_datetime_original)[0:4]
                    month = str(exif_datetime_original)[5:7]


        # None year and None month
        if year == "None" and month == "None":
            if os.path.exists(f"{PATH_SORTED}//None"):
                try:
                    if os.path.exists(f"{PATH_SORTED}//None//{image_name}"):
                        log.warning(f"{image_name} already here!")
                        count_duplicates_stuck += 1
                    else:
                        shutil.copy(image, f"{PATH_SORTED}//None//{image_name}")
                        log.warning(f"{image_name} - don't have EXIF date!")
                        count_sorted_with_none += 1
                except WindowsError as error:
                    log.warning(error)

            elif not os.path.exists("None"):
                os.makedirs(f"{PATH_SORTED}//None")
                log.warning(f"{PATH_SORTED_READABLE}/None - folder created!")
                try:
                    shutil.copy(image, f"{PATH_SORTED}//None//{image_name}")
                    log.warning(f"{image_name} - don't have EXIF date!")
                    count_sorted_with_none += 1
                except WindowsError as error:
                    log.warning(error)

        # create folder & move photos by year/month
        else:
            if os.path.exists(f"{PATH_SORTED}//{year}//{month}"):
                try:
                    if os.path.exists(
                            f"{PATH_SORTED}//{year}//{month}//{image_name}"):
                        log.warning(f"{image_name} already here!")
                        count_duplicates_stuck += 1
                    else:
                        shutil.copy(image, 
                            f"{PATH_SORTED}//{year}//{month}//{image_name}")
                        log.warning(f"{image_name} - sorted!")
                        count_sorted_with_date += 1
                except WindowsError as error:
                    log.warning(error)

            elif not os.path.exists(f"{PATH_SORTED}//{year}//{month}"):
                os.makedirs(f"{PATH_SORTED}//{year}//{month}")
                log.warning(f"{PATH_SORTED_READABLE}/{year}/{month} - folder created!")
                try:
                    shutil.copy(image, 
                                f"{PATH_SORTED}//{year}//{month}//{image_name}")
                    log.warning(f"{image_name} - sorted!")
                    count_sorted_with_date += 1
                except WindowsError as error:
                    log.warning(error)


log.warning(
    f"Number of unsorted images in {PATH_UNSORTED_READABLE}: {len(all_images_list)}\n" + \
    (" " * 20) + f" Number of sorted images into {PATH_SORTED_READABLE}: " + \
    f"{count_sorted_with_none + count_sorted_with_date}\n" + \
    (" " * 20) + f" Number of sorted images with date: {count_sorted_with_date}\n" + \
    (" " * 20) + f" Number of sorted images without date: {count_sorted_with_none}\n" + \
    (" " * 20) + f" Number of passes when duplicate finded: {count_duplicates_stuck}"
)

log.warning(f"{(time.time() - start_time)/60:.2f} minutes ({(time.time() - start_time)/60/60:.1f} hours)")

print("Press Ctrl+C to Exit!")
