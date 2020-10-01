#!/bin/sh
set -e
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py initcontent
uwsgi --ini ./compose/testing/uwsgi.ini
