FROM ckan/ckan-base:2.11.3

# Variables necesarias
ENV CKAN_SITE_URL=http://localhost:5000

# Copiamos el archivo de configuración
COPY ckan.ini /etc/ckan/ckan.ini

# Copiamos el entrypoint a una ubicación editable
COPY entrypoint.sh /srv/app/entrypoint.sh
RUN chmod +x /srv/app/entrypoint.sh

# Punto de entrada del contenedor
ENTRYPOINT ["/srv/app/entrypoint.sh"]
