#!/usr/bin/env bash
export CKAN_INI=ckan.ini

# Usar el puerto que Render asigna
PORT=${PORT:-5000}

cd src/ckan
python3 setup.py develop
python3 -m paste.script.serve ../../ckan.ini --port=$PORT
