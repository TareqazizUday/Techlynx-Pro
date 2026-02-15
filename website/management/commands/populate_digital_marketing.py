"""
Management command to populate Digital Marketing page data and download icons
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from website.models import (
    DigitalMarketingHero, DigitalMarketingService, DigitalMarketingStrategy,
    DigitalMarketingTestimonial, DigitalMarketingMetric, DigitalMarketingCTA
)
import requests

class Command(BaseCommand):
    help = 'Populate Digital Marketing page data and download icons'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating Digital Marketing page...'))
        
        # Create Hero Section
        hero, created = DigitalMarketingHero.objects.get_or_create(
            id=1,
            defaults={
                'badge_text': 'ROI-Focused Growth',
                'badge_icon': 'trending_up',
                'headline': 'Scale Your Business with <span class="text-primary">Strategy-First</span> Marketing',
                'description': 'High-performance, SEO-first digital growth services designed for measurable ROI. We help US-based brands dominate their niche through data-backed execution.',
                'cta_primary_text': 'Start Your Growth Journey',
                'cta_primary_url': '/contact',
                'cta_secondary_text': 'View Case Studies',
                'cta_secondary_url': '/case-studies',
                'growth_percentage': 248,
                'avg_cpc_reduction': 1.45,
                'conversion_rate': 8.4,
            }
        )
        
        # Create Services with icons
        services_data = [
            {
                'icon': 'search',
                'title': 'SEO Optimization',
                'description': 'Drive sustainable organic visibility and dominate long-term authority in your niche market.',
                'feature_1': 'Technical Audit',
                'feature_2': 'Backlink Engineering',
                'order': 1,
            },
            {
                'icon': 'ads_click',
                'title': 'SEM & PPC',
                'description': 'Instant lead generation with high-precision Google & Bing Ad campaigns backed by data.',
                'feature_1': 'Keyword Research',
                'feature_2': 'Bid Management',
                'order': 2,
            },
            {
                'icon': 'group',
                'title': 'Social Media',
                'description': 'Build community and brand authority across LinkedIn, Meta, and Twitter with targeted content.',
                'feature_1': 'Content Strategy',
                'feature_2': 'Paid Social Funnels',
                'order': 3,
            },
            {
                'icon': 'campaign',
                'title': 'Influencer Outreach',
                'description': 'Leverage trust and massive reach through strategic partnerships with top industry creators.',
                'feature_1': 'Talent Sourcing',
                'feature_2': 'Campaign Tracking',
                'order': 4,
            },
        ]
        
        # Service icons from Flaticon
        service_icons = {
            'SEO Optimization': 'https://cdn-icons-png.flaticon.com/512/2906/2906206.png',
            'SEM & PPC': 'https://cdn-icons-png.flaticon.com/512/3039/3039393.png',
            'Social Media': 'https://cdn-icons-png.flaticon.com/512/3037/3037485.png',
            'Influencer Outreach': 'https://cdn-icons-png.flaticon.com/512/2965/2965280.png',
        }
        
        self.stdout.write('\nCreating services and downloading icons...')
        for service_data in services_data:
            service, created = DigitalMarketingService.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            
            # Download icon if not present
            if not service.icon_image and service.title in service_icons:
                icon_url = service_icons[service.title]
                filename = f"{service.title.lower().replace(' ', '_').replace('&', 'and')}.png"
                icon_file = self.download_image(icon_url, filename)
                if icon_file:
                    service.icon_image.save(filename, icon_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f'✓ {service.title}: Icon added'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ {service.title}: Download failed'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ {service.title}: Icon exists'))
        
        # Create Strategy Steps
        strategy_steps_data = [
            {
                'step_number': 1,
                'title': 'Data Audit & Discovery',
                'description': 'We analyze your current metrics, competitor landscape, and market opportunities to find the "low hanging fruit" for rapid ROI.',
                'order': 1,
            },
            {
                'step_number': 2,
                'title': 'Custom Roadmap Engineering',
                'description': 'No cookie-cutter plans. We build a multi-channel funnel designed specifically to convert your high-value target audience.',
                'order': 2,
            },
            {
                'step_number': 3,
                'title': 'Agile Execution & Scaling',
                'description': 'Continuous A/B testing and optimization to lower acquisition costs while increasing lead quality and volume.',
                'order': 3,
            },
        ]
        
        for step_data in strategy_steps_data:
            DigitalMarketingStrategy.objects.get_or_create(
                step_number=step_data['step_number'],
                defaults=step_data
            )
        
        # Create Testimonials (using placeholder URLs - will be replaced with real photos)
        testimonials_data = [
            {
                'client_name': 'Marcus Thorne',
                'client_position': 'CEO',
                'client_company': 'Nexus Cloud',
                'testimonial_text': 'Techlynx Pro didn\'t just give us traffic; they gave us buyers. Our lead cost dropped 40% in just 3 months.',
                'order': 1,
            },
            {
                'client_name': 'Sarah Jenkins',
                'client_position': 'Marketing Director',
                'client_company': '',
                'testimonial_text': 'Their SEO strategy is like nothing we\'ve seen. We now rank #1 for our most competitive terms.',
                'order': 2,
            },
        ]
        
        for testimonial_data in testimonials_data:
            DigitalMarketingTestimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                defaults=testimonial_data
            )
        
        # Create Growth Metrics
        metrics_data = [
            {
                'title': 'Organic Impressions',
                'growth_indicator': '+12%',
                'chart_data': '20,35,30,50,85',
                'order': 1,
            },
            {
                'title': 'Conversion Value',
                'growth_indicator': '+$42k',
                'chart_data': '10,25,45,60,90',
                'order': 2,
            },
            {
                'title': 'Paid Search ROI',
                'growth_indicator': '4.2x',
                'chart_data': '40,30,55,45,80',
                'order': 3,
            },
        ]
        
        for metric_data in metrics_data:
            DigitalMarketingMetric.objects.get_or_create(
                title=metric_data['title'],
                defaults=metric_data
            )
        
        # Create CTA Section
        cta, created = DigitalMarketingCTA.objects.get_or_create(
            id=1,
            defaults={
                'icon': 'insights',
                'headline': 'Ready to see these results for yourself?',
                'description': 'Schedule a 15-minute strategy call and we\'ll show you exactly how we\'d grow your specific brand.',
                'cta_text': 'Book Your Free Strategy Call',
                'cta_url': '/contact',
            }
        )
        
        self.stdout.write(self.style.SUCCESS('\n✅ Digital Marketing page data populated successfully!'))

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
