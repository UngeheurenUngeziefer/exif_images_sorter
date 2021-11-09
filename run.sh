#!/bin/bash
source exif_sorter_venv/Scripts/activate
python exif_sorter.py

trap "sleep infinity" EXIT