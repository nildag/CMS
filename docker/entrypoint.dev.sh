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
python manage.py flush --no-input
python manage.py makemigrations categorias
python manage.py makemigrations contenido
python manage.py makemigrations permiso
python manage.py makemigrations rol
python manage.py makemigrations usuario
python manage.py migrate

python manage.py loaddata fixtures/permiso.json

# Creamos el superuser
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=admin12345 DJANGO_SUPERUSER_EMAIL=admin@example.com python manage.py createsuperuser --noinput

# Corremos el proyecto
python manage.py runserver 0.0.0.0:8000

exec "$@"
