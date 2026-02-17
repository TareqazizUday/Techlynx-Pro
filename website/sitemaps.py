from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost, CaseStudy


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return [
            'home',
            'about',
            'services',
            'web_development',
            'digital_marketing',
            'ai_solutions',
            'app_development',
            'seo_audit',
            'project_management',
            'finance_accounting',
            'content_production',
            'virtual_assistance',
            'industries',
            'case_studies',
            'blog',
            'all_blogs',
            'careers',
            'testimonials',
            'contact',
            'privacy_policy',
            'terms_of_service',
        ]

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(is_published=True).order_by('-published_date')

    def location(self, obj):
        return reverse('blog_detail', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class CaseStudySitemap(Sitemap):
    """Sitemap for case studies"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return CaseStudy.objects.filter(is_active=True).order_by('-created_at')

    def location(self, obj):
        return reverse('case_study_detail', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.created_at

