#!/usr/bin/env bash
export CKAN_INI=ckan.ini
cd src/ckan
python3 -m ckan.cli serve ../../ckan.ini
