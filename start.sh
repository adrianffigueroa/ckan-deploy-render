#!/usr/bin/env bash
export CKAN_INI=ckan.ini
gunicorn --paste $CKAN_INI
