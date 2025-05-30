FROM ckan/ckan-base:2.11.3

ENV CKAN_SITE_URL=http://localhost:5000

COPY ckan.ini /etc/ckan/ckan.ini

# Copiamos el script a /tmp donde sí tenemos permisos
COPY entrypoint.sh /tmp/entrypoint.sh

# El chmod falla si no estamos en /tmp
RUN chmod +x /tmp/entrypoint.sh

# Ejecutamos CKAN desde el script
ENTRYPOINT ["/tmp/entrypoint.sh"]
