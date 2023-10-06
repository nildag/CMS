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
python manage.py loaddata fixtures/rol.json
python manage.py loaddata fixtures/categorias.json
python manage.py loaddata fixtures/socialaccountapp.json

# Recoleta todos los archivos estaticos de todas las app y los agrupa en una carpeta staticfiles
python manage.py collectstatic

# Copiamos los archivos estaticos generado en el paso anterior a la carpeta static para que nginx pueda servirlos
cp -r staticfiles/. static

# Creamos el superuser
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=admin12345 DJANGO_SUPERUSER_EMAIL=admin@example.com python manage.py createsuperuser --noinput

exec "$@"
