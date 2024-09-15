#!/bin/bash

echo "Run migrations"
python manage.py collectstatic --no-input
python manage.py migrate

echo "Loading fixtures"
python manage.py loaddata ./apps/smakolyk/fixtures/first_menu.json

export DJANGO_TEST_DB_REMOVAL=yes
if python manage.py test --failfast --no-input; then
    echo "------------------------------------------------------"
    echo " Django tests passed"
    echo "------------------------------------------------------"
else
    echo "------------------------------------------------------"
    echo " Django tests failed"
    echo "------------------------------------------------------"
    exit
fi

echo "Starting the server..."
exec "$@"

gunicorn -c gunicorn/conf.py core.wsgi:application