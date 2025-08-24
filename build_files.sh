#!/bin/bash
# Force update

python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput