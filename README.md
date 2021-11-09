### What is that?
exif_sorter - is a little script that helps you sort photos by year and month 
from unsorted folders to year-month structure automatically. Script creates 
folder for each year and each month inside yead folder. If photo doesn't have
EXIF data photo will stored in None folder. All photos copying! 
Script can't delete anything!

### How to use
1) Install Python 3.10.0 (most likely usable with any Python3)
2) Pull this repo
3) Open "pathes.yaml" and change pathes to yours:
PATH_UNSORTED: 'D:\unsorted' - path to folder with any number, any hierarchy 
							   of folders and photos, that you need to sort in
							   year-month manner
PATH_SORTED: 'D:\sorted' - path where *exif_sorter* place sorted structured 
						   files
4) Click run.sh
5) After script finish working you can check logs in "logs/" folder