#!/bin/bash
py -m venv exif_sorter_venv
ls exif_sorter_venv/Scripts
source exif_sorter_venv/Scripts/activate
where python
pip install -r requirements.txt