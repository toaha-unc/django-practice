#!/bin/bash
# Build script for Vercel deployment

echo "Building Django application..."

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files for WhiteNoise
python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"
