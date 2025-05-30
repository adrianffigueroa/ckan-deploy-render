FROM ckan/ckan-base:2.11.3

ENV CKAN_SITE_URL=http://localhost:5000

# Copiamos el archivo de configuración
COPY ckan.ini /etc/ckan/ckan.ini

# Copiamos el script (sin chmod)
COPY entrypoint.sh /srv/app/entrypoint.sh

# ENTRYPOINT sin necesidad de permisos de ejecución
ENTRYPOINT ["/bin/bash", "/srv/app/entrypoint.sh"]
