#!/bin/sh

# Entry point spesific settings file
settings_entrypoint=$1

# Run using gunicorn from docker-entrypoint, bind to internal port 8080
DJANGO_SETTINGS_MODULE=$settings_entrypoint gunicorn sip.wsgi:application --bind 0.0.0.0:8000
