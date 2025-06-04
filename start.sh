#!/usr/bin/env bash
export CKAN_INI=ckan.ini
cd src/ckan
python3 setup.py develop
paster serve ../../ckan.ini
