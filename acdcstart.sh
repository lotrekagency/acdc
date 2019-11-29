#!/bin/bash

# Migrate the database
while !</dev/tcp/$DB_HOST/5432; do sleep 1; done;

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py run_huey --logfile huey_logs.log &> /dev/null &

./gunicorn.sh start
