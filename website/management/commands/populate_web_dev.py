"""
Management command to populate Web Development page data and download technology logos
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from website.models import (
    WebDevHero, WebDevService, WebDevStackFeature, WebDevTechnology,
    WebDevProcess, WebDevSEOBenefit, WebDevSEOMetric, WebDevCTA
)
import requests

class Command(BaseCommand):
    help = 'Populate Web Development page data and download technology logos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating Web Development page...'))
        
        # Technology logos (SVG format)
        tech_logos = {
            'Next.js': 'https://cdn.svgporn.com/logos/nextjs-icon.svg',
            'React': 'https://cdn.svgporn.com/logos/react.svg',
            'Tailwind': 'https://cdn.svgporn.com/logos/tailwindcss-icon.svg',
            'Node.js': 'https://cdn.svgporn.com/logos/nodejs-icon.svg',
            'Postgres': 'https://cdn.svgporn.com/logos/postgresql.svg',
            'AWS': 'https://cdn.svgporn.com/logos/aws.svg',
        }
        
        # Download and create technologies
        self.stdout.write('\nDownloading technology logos...')
        for idx, (tech_name, logo_url) in enumerate(tech_logos.items(), start=1):
            tech, created = WebDevTechnology.objects.get_or_create(
                name=tech_name,
                defaults={'order': idx}
            )
            
            if not tech.logo:
                logo_file = self.download_image(logo_url, f'{tech_name.lower().replace(".", "")}.svg')
                if logo_file:
                    tech.logo.save(f'{tech_name.lower().replace(".", "")}.svg', logo_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f'✓ {tech_name}: Logo downloaded'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ {tech_name}: Download failed'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ {tech_name}: Logo already exists'))
        
        # Create Hero Section
        hero, created = WebDevHero.objects.get_or_create(
            id=1,
            defaults={
                'badge_text': 'US-Based Enterprise Agency',
                'headline': 'Scalable, <span class="text-primary">SEO-First</span> Web Development',
                'description': 'High-performance websites built with Next.js and WordPress to drive ROI. Get a future-proof digital presence that converts visitors into loyal customers.',
                'cta_primary_text': 'Book a Free Consultation',
                'cta_primary_url': '/contact',
                'cta_secondary_text': 'View Case Studies',
                'cta_secondary_url': '/case-studies',
            }
        )
        
        # Create Services
        services_data = [
            {
                'icon': 'terminal',
                'title': 'Custom Full-Stack Development',
                'description': 'Bespoke web applications built for performance, security, and extreme scalability. We leverage Next.js, Node.js, and modern databases to deliver enterprise-grade software.',
                'feature_1': 'API Integration & Microservices',
                'feature_2': 'Server-Side Rendering (SSR)',
                'order': 1,
            },
            {
                'icon': 'shopping_cart',
                'title': 'Scalable E-commerce Solutions',
                'description': 'Conversion-optimized online stores designed to handle high traffic and provide seamless shopping experiences. From headless Shopify to custom WooCommerce architectures.',
                'feature_1': 'Multi-currency & Localization',
                'feature_2': 'Advanced Analytics Integration',
                'order': 2,
            },
        ]
        
        for service_data in services_data:
            WebDevService.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
        
        # Create Stack Features
        stack_features_data = [
            {
                'icon': 'bolt',
                'title': 'Next.js for Performance',
                'description': 'Lightning-fast page loads and automatic SEO optimization out of the box.',
                'order': 1,
            },
            {
                'icon': 'edit_note',
                'title': 'Headless WordPress',
                'description': 'Familiar content management with a decoupled frontend for superior speed.',
                'order': 2,
            },
            {
                'icon': 'database',
                'title': 'Modern Data Architecture',
                'description': 'PostgreSQL, MongoDB, and Redis for high-availability data handling.',
                'order': 3,
            },
        ]
        
        for feature_data in stack_features_data:
            WebDevStackFeature.objects.get_or_create(
                title=feature_data['title'],
                defaults=feature_data
            )
        
        # Create Process Steps
        process_steps_data = [
            {
                'step_number': 1,
                'title': 'Discovery',
                'description': 'Deep dive into your business goals, target audience, and technical requirements to build a roadmap.',
                'order': 1,
            },
            {
                'step_number': 2,
                'title': 'Design',
                'description': 'UI/UX design focused on conversion rate optimization and brand alignment across all devices.',
                'order': 2,
            },
            {
                'step_number': 3,
                'title': 'Build',
                'description': 'Agile development using our high-performance tech stack with continuous integration and testing.',
                'order': 3,
            },
            {
                'step_number': 4,
                'title': 'Launch',
                'description': 'Meticulous QA, deployment to production, and long-term performance monitoring and support.',
                'order': 4,
            },
        ]
        
        for step_data in process_steps_data:
            WebDevProcess.objects.get_or_create(
                step_number=step_data['step_number'],
                defaults=step_data
            )
        
        # Create SEO Benefits
        seo_benefits_data = [
            {
                'icon': 'speed',
                'title': 'Core Web Vitals',
                'description': '90+ Lighthouse scores across all devices.',
                'order': 1,
            },
            {
                'icon': 'schema',
                'title': 'Rich Schema',
                'description': 'Automated JSON-LD for rich search results.',
                'order': 2,
            },
            {
                'icon': 'responsive_layout',
                'title': 'Mobile-First',
                'description': 'Pixel-perfect performance on any screen size.',
                'order': 3,
            },
            {
                'icon': 'security',
                'title': 'Secure by Design',
                'description': 'SSL, WAF, and best-in-class security headers.',
                'order': 4,
            },
        ]
        
        for benefit_data in seo_benefits_data:
            WebDevSEOBenefit.objects.get_or_create(
                title=benefit_data['title'],
                defaults=benefit_data
            )
        
        # Create SEO Metrics
        seo_metrics_data = [
            {'metric_name': 'Performance', 'score': 100, 'color': 'green-400', 'order': 1},
            {'metric_name': 'Accessibility', 'score': 98, 'color': 'green-400', 'order': 2},
            {'metric_name': 'Best Practices', 'score': 100, 'color': 'green-400', 'order': 3},
            {'metric_name': 'SEO', 'score': 100, 'color': 'green-400', 'order': 4},
        ]
        
        for metric_data in seo_metrics_data:
            WebDevSEOMetric.objects.get_or_create(
                metric_name=metric_data['metric_name'],
                defaults=metric_data
            )
        
        # Create CTA Section
        cta, created = WebDevCTA.objects.get_or_create(
            id=1,
            defaults={
                'headline': 'Ready to Scale Your Online Presence?',
                'description': 'Join dozens of US enterprises who have transformed their digital ROI with our SEO-first development approach.',
                'cta_primary_text': 'Book Free Consultation',
                'cta_primary_url': '/contact',
                'cta_secondary_text': 'Contact Sales',
                'cta_secondary_url': '/contact',
                'footer_text': 'No credit card required. Initial consult is 100% free.',
            }
        )
        
        self.stdout.write(self.style.SUCCESS('\n✅ Web Development page data populated successfully!'))

    def download_image(self, url, filename):
        """Download image from URL"""
        try:
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            if response.status_code == 200:
                return ContentFile(response.content, name=filename)
            else:
                self.stdout.write(self.style.WARNING(f'Failed to download {filename}: Status {response.status_code}'))
                return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Error downloading {filename}: {str(e)}'))
            return None
