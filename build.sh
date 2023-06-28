#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata b-dumpdata-python.json
