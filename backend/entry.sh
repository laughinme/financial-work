#!/usr/bin/env bash
set -e

echo "Running Alembic migrations..."
cd src
alembic upgrade head
cd ..

echo "Starting the application..."
python -m src
