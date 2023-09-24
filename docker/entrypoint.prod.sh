#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Realizamos las migraciones
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/permiso.json

# Recoleta todos los archivos estaticos de todas las app en uno solo que se puede llamar asstes (directorio raiz del proyecto), este servira como directorio para una estructura del tipo app1/static app2/static. Como nosotros solo tenemos un directorio static en la raiz del proyecto en el que van todos los arhivos staticos organizados de la siguiente manera : raiz_proyecto/static/app1 raiz_proyecto/static/app1 ...., no necesitamos usar esta directiva
# python manage.py collectstatic

# Creamos el superuser
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=admin12345 DJANGO_SUPERUSER_EMAIL=admin@example.com python manage.py createsuperuser --noinput

exec "$@"
