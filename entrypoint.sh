#!/usr/bin/env bash

echo "Run migrations"
python flatapp/manage.py migrate

echo "Running app: $@"
exec "$@"
