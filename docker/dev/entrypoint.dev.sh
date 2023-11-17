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

# Cargamos los datos iniciales
python manage.py loaddata fixtures/permiso.json
python manage.py loaddata fixtures/rol.json
python manage.py loaddata fixtures/categorias.json
python manage.py loaddata fixtures/socialaccountapp.json
# python manage.py loaddata fixtures/userCategoria.json

# Corremos el proyecto
python manage.py runserver 0.0.0.0:8000

exec "$@"
