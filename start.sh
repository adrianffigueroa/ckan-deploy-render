#!/usr/bin/env bash
export CKAN_INI=ckan.ini
cd src/ckan
python3 setup.py develop
python3 -m paste.script.serve ../../ckan.ini
