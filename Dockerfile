# Imagen base oficial de CKAN
FROM ckan/ckan-base:2.11.3

# Seteamos variables necesarias para CKAN
ENV CKAN_SITE_URL=http://localhost:5000

# Copiamos el archivo de configuración
COPY ckan.ini /etc/ckan/ckan.ini

# Instalamos dependencias adicionales si existen
COPY requirements.txt /srv/app/requirements.txt
RUN pip install -r /srv/app/requirements.txt || echo "No se encontraron requerimientos adicionales"

# Comando por defecto para ejecutar CKAN
CMD ["ckan", "run", "-c", "/etc/ckan/ckan.ini"]
