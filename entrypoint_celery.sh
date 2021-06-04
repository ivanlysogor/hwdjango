#!/usr/bin/env bash

echo "Running app: Celery"
cd /var/app/flatapp
celery -A flatapp worker -B -l INFO
