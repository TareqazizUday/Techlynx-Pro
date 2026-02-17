# Techlynx Pro - Django Website

Professional Django website for Techlynx Pro IT Services company.

## How to Run the Project

### Quick Start

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create Admin User (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Server**
   ```bash
   python manage.py runserver
   ```

7. **Open in Browser**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

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
- **Database**: SQLite (development)
- **Fonts**: Google Fonts (Inter)

## Project Structure

```
techlynx_project/
├── techlynx_project/        # Project settings
├── website/                 # Main app
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── manage.py              # Django management
└── requirements.txt        # Dependencies
```

## Pages

- **Home** (`/`) - Landing page
- **About** (`/about/`) - Company information
- **Services** (`/services/`) - Services overview
- **Web Development** (`/services/web-development/`)
- **Digital Marketing** (`/services/digital-marketing/`)
- **AI Solutions** (`/services/ai-solutions/`)
- **App Development** (`/services/app-development/`)
- **SEO Audit** (`/services/seo-audit/`)
- **Project Management** (`/services/project-management/`)
- **Finance & Accounting** (`/services/finance-accounting/`)
- **Content Production** (`/services/content-production/`)
- **Virtual Assistance** (`/services/virtual-assistance/`)
- **Industries** (`/industries/`)
- **Case Studies** (`/case-studies/`)
- **Blog** (`/blog/`)
- **Careers** (`/careers/`)
- **Testimonials** (`/testimonials/`)
- **Contact** (`/contact/`)

## License

© 2025 Techlynx Pro. All rights reserved.
