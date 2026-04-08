from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from .models import BlogPost, CaseStudy


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages - helps Google index all main pages."""
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https' if not getattr(settings, 'DEBUG', True) else None  # HTTPS in production for canonical URLs

    def items(self):
        return [
            'home',
            'about',
            'services',
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
            'case_studies',
            'blog',
            'all_blogs',
            'careers',
            'testimonials',
            'privacy_policy',
            'terms_of_service',
        ]

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    """Sitemap for blog posts."""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https' if not getattr(settings, 'DEBUG', True) else None

    def items(self):
        return BlogPost.objects.filter(is_published=True).order_by('-published_date')

    def location(self, obj):
        return reverse('blog_detail', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class CaseStudySitemap(Sitemap):
    """Sitemap for case studies."""
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https' if not getattr(settings, 'DEBUG', True) else None

    def items(self):
        return CaseStudy.objects.filter(is_active=True).order_by('-created_at')

    def location(self, obj):
        return reverse('case_study_detail', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.created_at

