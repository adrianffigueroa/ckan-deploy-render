#!/usr/bin/env bash
export CKAN_INI=ckan.ini

# Usar Gunicorn con PasteDeploy
PORT=${PORT:-5000}
gunicorn --paste $CKAN_INI --bind 0.0.0.0:$PORT
