web: DJANGO_SETTINGS_MODULE=sip.settings.staging gunicorn sip.wsgi --log-file -
release: chmod 777 migrate.sh && ./migrate.sh