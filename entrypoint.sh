#!/bin/bash
set -e

# Exporta SECRET_KEY si no está seteado por algún motivo
export SECRET_KEY="${SECRET_KEY:-default-secret-key}"

# Ejecuta CKAN
ckan run -c /etc/ckan/ckan.ini
