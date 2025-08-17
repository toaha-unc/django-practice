# Vercel Deployment Guide

## Prerequisites
- Vercel account
- Supabase database (already configured)
- Git repository with your Django project

## Environment Variables for Vercel

Set these environment variables in your Vercel project settings:

```
user=postgres.iquxptnnslogwzxhkvbq
password=Bondstone1234!
host=aws-1-us-east-2.pooler.supabase.com
port=5432
dbname=postgres
```

## Deployment Steps

1. **Connect your repository to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your Git repository
   - Select the repository containing this Django project

2. **Configure environment variables**
   - In your Vercel project dashboard, go to Settings → Environment Variables
   - Add all the database environment variables listed above

3. **Deploy**
   - Vercel will automatically detect the Django project
   - The build process will:
     - Install dependencies from `requirements.txt`
     - Run database migrations
     - Collect static files
     - Deploy the application

## URLs After Deployment

Once deployed, your application will be available at:
- **Main site**: `https://django-practice-six.vercel.app`
- **Swagger UI**: `https://django-practice-six.vercel.app/swagger-ui/`
- **Swagger JSON**: `https://django-practice-six.vercel.app/swagger.json`
- **ReDoc**: `https://django-practice-six.vercel.app/redoc/`
- **Admin**: `https://django-practice-six.vercel.app/admin/`

## API Endpoints

### Authentication
- `POST /auth/jwt/create/` - Create JWT token
- `POST /auth/jwt/refresh/` - Refresh JWT token
- `POST /auth/jwt/verify/` - Verify JWT token

### Library Management
- `GET/POST /api/authors/` - Authors management
- `GET/POST /api/books/` - Books management
- `GET/POST /api/members/` - Members management
- `GET/POST /api/borrow-records/` - Borrow records management

## Testing the API

1. **Get JWT Token**:
   ```bash
   curl -X POST https://django-practice-six.vercel.app/auth/jwt/create/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
   ```

2. **Use the token**:
   ```bash
   curl -X GET https://django-practice-six.vercel.app/api/books/ \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify environment variables are set correctly
   - Check if Supabase database is accessible
   - Ensure SSL mode is enabled

2. **Static Files Not Loading**
   - Static files are collected during build
   - Check if `STATIC_ROOT` is properly configured
   - Verify Vercel routes are correct

3. **Migration Errors**
   - Ensure database is accessible
   - Check if all migrations are up to date
   - Verify database permissions

### Local Development

To run locally:
```bash
# Create .env file with your database credentials
echo "user=postgres.iquxptnnslogwzxhkvbq
password=Bondstone1234!
host=aws-1-us-east-2.pooler.supabase.com
port=5432
dbname=postgres" > .env

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## Security Notes

- Keep your database credentials secure
- Use environment variables for sensitive data
- Consider using Vercel's built-in environment variable encryption
- Regularly update dependencies for security patches
