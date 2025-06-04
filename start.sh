#!/usr/bin/env bash
export CKAN_INI=ckan.ini
cd src/ckan
python3 setup.py develop
cd ../..
PORT=${PORT:-5000}
gunicorn --paste $CKAN_INI --bind 0.0.0.0:$PORT
