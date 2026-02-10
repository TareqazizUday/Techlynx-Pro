# Techlynx Pro - Django Website

Professional Django website for Techlynx Pro IT Services company.

## Features

- ✅ Modern, responsive design with Tailwind CSS
- ✅ Dark mode support
- ✅ Contact form with database storage
- ✅ Newsletter subscription
- ✅ SEO-optimized architecture
- ✅ Professional admin panel
- ✅ Multiple service pages
- ✅ Case studies showcase
- ✅ Blog/Insights section
- ✅ Careers page

## Tech Stack

- **Backend**: Django 5.0
- **Frontend**: Tailwind CSS, Material Icons
- **Database**: SQLite (development), PostgreSQL recommended for production
- **Fonts**: Google Fonts (Inter)

## Installation & Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

### 7. Access Admin Panel

Visit: **http://127.0.0.1:8000/admin/**

Login with the superuser credentials you created.

## Project Structure

```
techlynx_project/
├── techlynx_project/        # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── website/                 # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin configuration
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── website/           # Page templates
├── static/                 # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── manage.py              # Django management
└── requirements.txt       # Dependencies
```

## Pages

- **Home** (`/`) - Landing page
- **About** (`/about/`) - Company information
- **Services** (`/services/`) - Services overview
- **Web Development** (`/services/web-development/`) - Web dev services
- **Digital Marketing** (`/services/digital-marketing/`) - Marketing services
- **Industries** (`/industries/`) - Industries served
- **Case Studies** (`/case-studies/`) - Success stories
- **Blog** (`/blog/`) - Insights & articles
- **Careers** (`/careers/`) - Job openings
- **Contact** (`/contact/`) - Contact form

## Database Models

### ContactInquiry
Stores contact form submissions with:
- Full name, email, service interest
- Budget range, project details
- Timestamp

### Newsletter
Manages newsletter subscriptions:
- Email address
- Subscription status
- Timestamp

## Customization

### Update Colors
Edit Tailwind configuration in `templates/base.html`:
```javascript
colors: {
    "primary": "#136dec",  // Change this
    ...
}
```

### Add New Pages
1. Create view in `website/views.py`
2. Add URL in `website/urls.py`
3. Create template in `templates/website/`

### Modify Contact Form
Edit the `ContactInquiry` model in `website/models.py` and run:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

### Settings for Production

In `techlynx_project/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Uncomment security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Collect Static Files

```bash
python manage.py collectstatic
```

### Database

Switch to PostgreSQL for production:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Support

For issues or questions, contact the development team.

## License

© 2024 Techlynx Pro. All rights reserved.
