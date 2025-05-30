#!/bin/bash
set -e

export SECRET_KEY="${SECRET_KEY:-default-secret-key}"

ckan run -c /etc/ckan/ckan.ini
