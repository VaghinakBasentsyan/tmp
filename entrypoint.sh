#!/bin/bash

FOLDER="/app"

# Wait for Postgres to be ready
#for _ in `seq 0 100`; do
#    (echo > /dev/tcp/${DB_NAME}/${DB_PORT}) >/dev/null 2>&1
#    if [[ $? -eq 0 ]]; then
#        printf " done!\n"
#        break
#    fi
#    echo "Waiting for Postgres..."
#    sleep 1
#done#
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin');
"

python manage.py collectstatic --noinput
python manage.py generate_dummy_data

python manage.py runserver 0.0.0.0:8000
