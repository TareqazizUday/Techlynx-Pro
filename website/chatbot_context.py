"""
Chatbot Context Extraction System
Extracts and caches text content from all website templates for Gemini AI chatbot
"""

import os
from pathlib import Path
from django.conf import settings
from bs4 import BeautifulSoup
import re

# Global cache for extracted context
_cached_context = None


def strip_html_tags(html_content):
    """
    Remove HTML tags and extract readable text from HTML content
    """
    # Remove script and style elements
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style tags
    for script in soup(['script', 'style', 'nav', 'footer', 'header']):
        script.decompose()
    
    # Get text
    text = soup.get_text(separator=' ', strip=True)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    
    return text.strip()


def extract_template_content(template_name):
    """
    Extract text content from a specific template file
    """
    template_path = Path(settings.BASE_DIR) / 'templates' / 'website' / template_name
    
    if not template_path.exists():
        return ""
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Remove Django template tags for cleaner extraction
        html_content = re.sub(r'{%.*?%}', '', html_content)
        html_content = re.sub(r'{{.*?}}', '', html_content)
        
        # Extract text
        text = strip_html_tags(html_content)
        
        return text
    except Exception as e:
        print(f"Error extracting content from {template_name}: {e}")
        return ""


def extract_documentation():
    """
    Extract content from documentation files (README, PROJECT_SUMMARY)
    """
    docs_content = []
    
    doc_files = ['README.md', 'PROJECT_SUMMARY_BANGLA.md']
    
    for doc_file in doc_files:
        doc_path = Path(settings.BASE_DIR) / doc_file
        if doc_path.exists():
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Take first 500 characters of each doc (summary only)
                    docs_content.append(content[:500])
            except Exception as e:
                print(f"Error reading {doc_file}: {e}")
    
    return "\n\n".join(docs_content)


def extract_site_context():
    """
    Extract and organize all website content for chatbot context
    Returns formatted string with all site information
    """
    context_parts = []
    
    # Company Overview
    context_parts.append("=== TECHLYNX PRO - COMPANY OVERVIEW ===")
    about_content = extract_template_content('about.html')
    if about_content:
        context_parts.append(about_content[:1500])  # First 1500 chars
    
    # Services Overview
    context_parts.append("\n\n=== SERVICES OVERVIEW ===")
    services_content = extract_template_content('services.html')
    if services_content:
        context_parts.append(services_content[:2000])
    
    # Detailed Service Pages
    service_pages = {
        'AI Solutions': 'ai-solutions.html',
        'Web Development': 'web-development.html',
        'Digital Marketing': 'digital-marketing.html',
        'App Development': 'app-development.html',
        'SEO Audit': 'seo-audit.html',
        'Project Management': 'project-management.html',
        'Finance & Accounting': 'finance-accounting.html',
        'Content Production': 'content-production.html',
    }
    
    for service_name, template_name in service_pages.items():
        context_parts.append(f"\n\n=== SERVICE: {service_name.upper()} ===")
        content = extract_template_content(template_name)
        if content:
            # Take first 1200 characters of each service page
            context_parts.append(content[:1200])
    
    # Industries
    context_parts.append("\n\n=== INDUSTRIES WE SERVE ===")
    industries_content = extract_template_content('industries.html')
    if industries_content:
        context_parts.append(industries_content[:800])
    
    # Case Studies
    context_parts.append("\n\n=== CASE STUDIES & SUCCESS STORIES ===")
    case_studies_content = extract_template_content('case-studies.html')
    if case_studies_content:
        context_parts.append(case_studies_content[:800])
    
    # Contact Information
    context_parts.append("\n\n=== CONTACT INFORMATION ===")
    contact_content = extract_template_content('contact.html')
    if contact_content:
        context_parts.append(contact_content[:1000])
    
    # Careers
    context_parts.append("\n\n=== CAREERS & OPPORTUNITIES ===")
    careers_content = extract_template_content('careers.html')
    if careers_content:
        context_parts.append(careers_content[:600])
    
    # Combine all parts
    full_context = "\n".join(context_parts)
    
    # Add metadata
    metadata = f"""
WEBSITE: Techlynx Pro - Professional IT Services
LOCATION: United States
EMAIL: hello@techlynxpro.com
PHONE: +1 (520) 666-4699
BUSINESS HOURS: Monday-Friday, 9am-6pm EST

SERVICES OFFERED:
1. AI Solutions (Chatbots, Machine Learning, Computer Vision)
2. Web Development (Custom websites, E-commerce, Web Apps)
3. Digital Marketing (SEO, PPC, Social Media, Content Marketing)
4. App Development (iOS, Android, Cross-platform)
5. SEO Audit (Technical SEO, On-page, Backlink Analysis)
6. Project Management (Agile, Waterfall, Hybrid)
7. Finance & Accounting (Bookkeeping, Tax Prep, Virtual CFO)
8. Content Production (Blog Writing, Video, Graphics, Social Media)
9. Virtual Assistance (Administrative support)

PRICING RANGES:
- Small Projects: $5,000 - $10,000
- Medium Projects: $10,000 - $25,000
- Large Projects: $25,000 - $50,000
- Enterprise: $50,000+

"""
    
    return metadata + "\n\n" + full_context


def get_chatbot_context():
    """
    Get cached context or extract if not cached
    This is the main function to call from views
    """
    global _cached_context
    
    if _cached_context is None:
        print("Extracting site context for chatbot...")
        _cached_context = extract_site_context()
        print(f"Context extracted: {len(_cached_context)} characters")
    
    return _cached_context


def refresh_context():
    """
    Force refresh the cached context
    Call this when templates are updated
    """
    global _cached_context
    _cached_context = None
    return get_chatbot_context()
