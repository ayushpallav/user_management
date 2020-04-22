#! /bin/sh

cd /src/ || exit

echo "RUNNING MIGRATIONS" && python manage.py migrate

echo "MAKING SUPERUSER" && python manage.py initadmin

echo "COLLECT STATIC" && python manage.py collectstatic --noinput

echo "Server is about to get up Morty!" && gunicorn user_management.wsgi:application --bind 0.0.0.0:$PORT
