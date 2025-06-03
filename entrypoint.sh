#!/bin/sh

echo "⏳ Waiting for DB at $DB_HOST..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done

echo "✅ DB is up. Running migrations..."
python manage.py migrate

echo "🚀 Starting server..."
exec python manage.py runserver 0.0.0.0:$PORT
