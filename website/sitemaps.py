"""
Sitemaps for Google Search — canonical HTTPS URLs, accurate lastmod, sensible changefreq/priority hints.

Only include indexable public URLs (matches robots.txt: no /api/, /admin/, etc.).
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings

from .models import BlogPost, CaseStudy, JobOpening


class StaticViewSitemap(Sitemap):
    """Named URL routes: home, services, legal, etc."""

    protocol = 'https' if not getattr(settings, 'DEBUG', True) else None

    # Home + primary nav (menu) — highest priority for indexing hints
    _priority = {
        'home': 1.0,
        'services': 0.96,
        'case_studies': 0.96,
        'testimonials': 0.96,
        'about': 0.96,
        'careers': 0.96,
        'blog': 0.96,
        'contact': 0.9,
        'industries': 0.85,
        'all_blogs': 0.85,
    }
    _changefreq = {
        'home': 'weekly',
        'services': 'weekly',
        'case_studies': 'weekly',
        'testimonials': 'weekly',
        'about': 'weekly',
        'careers': 'weekly',
        'blog': 'weekly',
        'all_blogs': 'weekly',
        'privacy_policy': 'yearly',
        'terms_of_service': 'yearly',
    }

    def items(self):
        # Order: home → main nav pages Google Search Console cares about → rest
        return [
            'home',
            'services',
            'case_studies',
            'testimonials',
            'about',
            'careers',
            'blog',
            'all_blogs',
            'contact',
            'web_development',
            'digital_marketing',
            'ai_solutions',
            'app_development',
            'seo_audit',
            'project_management',
            'finance_accounting',
            'content_production',
            'virtual_assistance',
            'bpo',
            'industries',
            'privacy_policy',
            'terms_of_service',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self._priority.get(item, 0.8)

    def changefreq(self, item):
        return self._changefreq.get(item, 'monthly')


class BlogPostSitemap(Sitemap):
    """Published blog posts only."""

    changefreq = 'weekly'
    priority = 0.75
    protocol = 'https' if not getattr(settings, 'DEBUG', True) else None

    def items(self):
        return BlogPost.objects.filter(is_published=True).order_by('-published_date')

    def location(self, obj):
        return reverse('blog_detail', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class CaseStudySitemap(Sitemap):
    """Active case study detail pages."""

    changefreq = 'monthly'
    priority = 0.75
    protocol = 'https' if not getattr(settings, 'DEBUG', True) else None

    def items(self):
        return CaseStudy.objects.filter(is_active=True).order_by('-created_at')

    def location(self, obj):
        return reverse('case_study_detail', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.created_at


class CareersJobSitemap(Sitemap):
    """Job deep-links /careers/?job=<id> — only active openings."""

    changefreq = 'weekly'
    priority = 0.65
    protocol = 'https' if not getattr(settings, 'DEBUG', True) else None

    def items(self):
        return JobOpening.objects.filter(is_active=True).order_by('id')

    def location(self, obj):
        return f"{reverse('careers')}?job={obj.pk}"

    def lastmod(self, obj):
        return obj.updated_at
