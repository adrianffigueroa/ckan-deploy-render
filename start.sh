#!/usr/bin/env bash
export CKAN_INI=ckan.ini
cd src/ckan
paster serve ../../ckan.ini
