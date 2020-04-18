#! /bin/sh

cd /src/ || exit

echo "RUNNING MIGRATIONS" && python manage.py migrate

echo "MAKING SUPERUSER" && python manage.py initadmin

# echo "COLLECT STATIC" && python manage.py collectstatic --noinput

exec "$@"