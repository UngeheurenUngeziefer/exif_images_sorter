import os
from glob import glob
import exifread
import shutil
from PIL import Image

PATH_TO_SORT = r"C:\Users\sewer\Python\exif_sorter\test_dataset"
BASE_DIR = r"C:\Users\sewer\Python\exif_sorter"

# list of all .jpg files inside folder recursively
all_images_list = [y for x in os.walk(PATH_TO_SORT) 
                  for y in glob(os.path.join(x[0], '*.jpg'))]
print(f"Found {len(all_images_list)} images overall!")


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
            if os.path.exists(f"{BASE_DIR}\\None"):
                try:
                    print(f"{image_name} - don't have EXIF date!")
                    shutil.move(image, f"{BASE_DIR}\\None\\{image_name}")
                except WindowsError:
                    pass
            elif not os.path.exists("None"):
                os.makedirs(f"{BASE_DIR}\\None")
                print(f"{BASE_DIR}\\None - folder created!")
                try:
                    print(f"{image_name} - don't have EXIF date!")
                    shutil.move(image, f"{BASE_DIR}\\None\\{image_name}")
                except WindowsError:
                    pass

        # create folder & move photos by year/month
        else:
            if os.path.exists(f"{BASE_DIR}\\{year}\\{month}"):
                try:
                    print(f"{image_name} - sorted!")
                    shutil.move(image, 
                                f"{BASE_DIR}\\{year}\\{month}\\{image_name}")
                except WindowsError:
                    pass

            elif not os.path.exists(f"{BASE_DIR}\\{year}\\{month}"):
                os.makedirs(f"{BASE_DIR}\\{year}\\{month}")
                print(f"{BASE_DIR}\\{year}\\{month} - folder created!")
                try:
                    print(f"{image_name} - sorted!")
                    shutil.move(image, 
                                f"{BASE_DIR}\\{year}\\{month}\\{image_name}")
                except WindowsError:
                    pass
