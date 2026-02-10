# Techlynx Pro - Setup & Deployment Guide

## Quick Start (Windows)

### Automated Setup
Simply double-click `setup.bat` and follow the prompts!

### Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create and run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

## Quick Start (Mac/Linux)

### Automated Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create and run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

## Environment Variables Setup

### Required: Gemini API Key for Chatbot

The AI-powered chatbot requires a Google Gemini API key. Follow these steps:

1. **Get Your API Key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated key

2. **Configure Environment Variables:**
   
   The `.env` file already exists in your project root. Open it and update:

   ```env
   # Required for Chatbot
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   
   # Optional Django Settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

3. **Verify Setup:**
   - Run the development server
   - Click the chatbot icon (bottom-right corner)
   - Ask a test question like "What services do you offer?"
   - If configured correctly, you'll get an AI-powered response

**Note:** Without a valid Gemini API key, the chatbot will show "Chatbot is temporarily unavailable"

### Optional Environment Variables

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Chatbot Features

The Techlynx AI Assistant chatbot provides:
- **AI-Powered Responses**: Uses Google Gemini 2.5 Flash for intelligent answers
- **Site Context Awareness**: Trained on all 16 pages of your website
- **Rate Limiting**: 10 queries per hour per session
- **Session Persistence**: Chat history saved during browser session
- **Mobile Responsive**: Full-screen chat on mobile devices
- **Dark Mode Compatible**: Matches your site's theme

**Usage Limits:**
- Max 10 queries per hour per user
- Max 500 characters per message
- Responses typically in 2-4 seconds

**Cost Estimate:**
- ~$7.50/month for 1,000 queries/day (Gemini 2.5 Flash pricing)

## Common Commands

### Run Development Server
```bash
python manage.py runserver
```

### Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Run Tests
```bash
python manage.py test
```

## Database Management

### View All Data
Access the admin panel at: http://127.0.0.1:8000/admin/

### Export Data
```bash
python manage.py dumpdata > data.json
```

### Import Data
```bash
python manage.py loaddata data.json
```

## Production Deployment

### 1. Update Settings

Edit `techlynx_project/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 2. Set Up PostgreSQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'techlynx_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Install Production Server

```bash
pip install gunicorn
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --no-input
```

### 5. Run with Gunicorn

```bash
gunicorn techlynx_project.wsgi:application --bind 0.0.0.0:8000
```

## Deployment Platforms

### Heroku
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn techlynx_project.wsgi
   ```
3. Deploy:
   ```bash
   heroku create techlynx-pro
   git push heroku main
   heroku run python manage.py migrate
   ```

### DigitalOcean / AWS / Azure
- Use Nginx as reverse proxy
- Configure Gunicorn as WSGI server
- Set up SSL with Let's Encrypt
- Use managed database service

### Docker (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "techlynx_project.wsgi:application"]
```

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8080
```

### Database Locked
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
```

### Permission Denied (setup.sh)
```bash
chmod +x setup.sh
```

## Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Backup Database
```bash
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

### Clear Cache
```bash
python manage.py clear_cache
```

## Support

For technical support or questions:
- Check the README.md file
- Review Django documentation: https://docs.djangoproject.com/
- Contact: support@techlynxpro.com

---

© 2024 Techlynx Pro. All rights reserved.
