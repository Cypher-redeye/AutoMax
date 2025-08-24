#!/bin/bash

# build_files.sh
# This is the new, correct line
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput