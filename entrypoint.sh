#!/usr/bin/env bash

echo "Run migrations"
python flatapp/manage.py migrate

echo "Running app: Flatapp"
python flatapp/manage.py runserver 0.0.0.0:8000
