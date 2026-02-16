from django.core.management.base import BaseCommand
from website.models import TestimonialsPageHero, TestimonialsPageCTA


class Command(BaseCommand):
    help = 'Populate testimonials page hero and CTA sections with initial data'

    def handle(self, *args, **kwargs):
        # Create Hero Section
        hero, created = TestimonialsPageHero.objects.get_or_create(
            defaults={
                'badge_text': 'Client Success Stories',
                'headline': 'Real Clients.\nReal Results.',
                'subheadline': '(No Made-Up Quotes.)',
                'description': "We've been transforming businesses since our founding. Here's what industry leaders say about their experience working with Techlynx Pro—authentic testimonials from executives who've achieved measurable growth.",
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Testimonials Hero Section'))
        else:
            self.stdout.write(self.style.WARNING('→ Testimonials Hero already exists'))
        
        # Create CTA Section
        cta, created = TestimonialsPageCTA.objects.get_or_create(
            defaults={
                'badge_text': 'Ready to Start?',
                'headline': 'Join the Success Stories',
                'description': 'Ready to achieve similar results? Our team of experts is standing by to discuss your project and create a customized strategy that delivers measurable growth for your business.',
                'cta_primary_text': 'Start Your Success Story',
                'cta_primary_url': '/contact/',
                'cta_secondary_text': 'Schedule Consultation',
                'cta_secondary_url': 'tel:+1234567890',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Testimonials CTA Section'))
        else:
            self.stdout.write(self.style.WARNING('→ Testimonials CTA already exists'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Testimonials page dynamic content initialized!'))
        self.stdout.write(self.style.SUCCESS('📝 You can now edit these sections from the Django admin panel'))
