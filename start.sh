#!/usr/bin/env bash
export CKAN_INI=ckan.ini
cd src/ckan
../../.venv/bin/paster serve ../../ckan.ini
