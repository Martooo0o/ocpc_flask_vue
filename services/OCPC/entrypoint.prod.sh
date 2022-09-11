#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py create_db
#python -c 'from manage import create_db; create_db()'
gunicorn -b 0.0.0.0:5000 manage:app\
    --log-level DEBUG \
    --reload