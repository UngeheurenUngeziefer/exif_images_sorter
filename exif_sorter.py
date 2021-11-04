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
    
    print("#################################")
    print(f"Image name: {image_name}")
    with open(image, 'rb') as image_file:
        tags = exifread.process_file(image_file)

        # we dont have EXIF date info 
        if "EXIF DateTimeOriginal" not in tags.keys():
            print("None")
            year = "None"
            month = "None"
            print(f"year: {year}")
            print(f"month: {month}")

        # we have EXIF date info
        else:
            for tag in tags.keys():
                if tag == "EXIF DateTimeOriginal":
                    exif_datetime_original = tags[tag]
                    year = str(exif_datetime_original)[0:4]
                    month = str(exif_datetime_original)[5:7]
                    
                    print(tags[tag])
                    print(f"year: {str(exif_datetime_original)[0:4]}")
                    print(f"month: {str(exif_datetime_original)[5:7]}")


        # None year and None month fix
        if os.path.exists(f"{BASE_DIR}\\{year}"):
            # move image to this folder
            try:
                shutil.move(image, f"{BASE_DIR}\\{year}\\{image_name}")
            except WindowsError:
                pass
            # if os.path.exists(f"{year}/{month}):

        elif not os.path.exists(f"{BASE_DIR}\\{year}"):
            # create folder, then move image to this folder
            os.makedirs(f"{BASE_DIR}\\{year}")
            try:
                shutil.move(image, f"{BASE_DIR}\\{year}\\{image_name}")
            except WindowsError:
                pass

