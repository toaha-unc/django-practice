#!/bin/bash
# Build script for Vercel deployment

echo "Building Django application..."

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create test users and sample data
python manage.py create_test_users
python manage.py create_sample_data

# Collect static files for WhiteNoise
python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"
