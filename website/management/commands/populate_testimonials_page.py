from django.core.management.base import BaseCommand
from website.models import (
    TestimonialsPageSEO,
    TestimonialsPageHero,
    TestimonialsPageWhyChoose,
    TestimonialsPageWhyChooseReason,
    TestimonialsPageCTA
)


class Command(BaseCommand):
    help = 'Populates initial data for Testimonials page sections'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Populating Testimonials page content...'))
        
        # Create SEO
        seo, created = TestimonialsPageSEO.objects.get_or_create(
            defaults={
                'page_title': 'Client Testimonials | Real Results from Real Businesses',
                'meta_description': 'Read what our clients say about Techlynx Pro. Real testimonials from businesses we\'ve helped grow with AI solutions, web development, and digital marketing.',
                'meta_keywords': 'client testimonials, customer reviews, client success stories, business reviews, IT services reviews, web development testimonials, digital marketing reviews',
                'og_title': 'Real Clients. Real Results. | Techlynx Pro Testimonials',
                'og_description': 'Don\'t just take our word for it. See what businesses say about working with Techlynx Pro.',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Testimonials SEO'))
        else:
            self.stdout.write(self.style.WARNING('→ Testimonials SEO already exists'))
        
        # Create Hero
        hero, created = TestimonialsPageHero.objects.get_or_create(
            defaults={
                'badge_icon': 'rate_review',
                'badge_text': 'What Clients Say',
                'headline': 'Real Clients. Real Results.',
                'subheadline': '(No Made-Up Quotes.)',
                'description': 'We\'ve been helping businesses grow online since 2015. Here\'s what clients say about working with Techlynx Pro—straight from the people who\'ve actually worked with us.',
                'cta_text': 'Get Your Free Quote',
                'cta_url': '/contact/',
                'cta_icon': 'arrow_forward',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Testimonials Hero'))
        else:
            self.stdout.write(self.style.WARNING('→ Testimonials Hero already exists'))
        
        # Create Why Choose
        why_choose, created = TestimonialsPageWhyChoose.objects.get_or_create(
            defaults={
                'badge_icon': 'verified',
                'badge_text': 'Why Choose Techlynx Pro',
                'headline': 'Three Reasons Clients Stick With Us',
                'description': 'We deliver experienced digital development services tailored to your business goals. With 100+ satisfied clients, we\'ve proven our commitment to excellence.',
                'illustration_image': 'testimonials/illustrated/kim.png',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Why Choose Section'))
        else:
            self.stdout.write(self.style.WARNING('→ Why Choose Section already exists'))
        
        # Create Why Choose Reasons
        reasons_data = [
            {
                'title': '10+ Years of Experience',
                'description': 'Been figuring this out since 2015 so you don\'t have to',
                'order': 1,
                'is_default_open': True,
                'is_active': True,
            },
            {
                'title': 'Direct Communication',
                'description': 'Work with our team directly—no account managers, no runaround',
                'order': 2,
                'is_default_open': False,
                'is_active': True,
            },
            {
                'title': 'Proven Results',
                'description': '500+ completed projects and 100+ happy clients since inception',
                'order': 3,
                'is_default_open': False,
                'is_active': True,
            },
        ]
        
        reason_count = 0
        for reason_data in reasons_data:
            reason, created = TestimonialsPageWhyChooseReason.objects.get_or_create(
                title=reason_data['title'],
                defaults=reason_data
            )
            if created:
                reason_count += 1
        
        if reason_count > 0:
            self.stdout.write(self.style.SUCCESS(f'✓ Created {reason_count} Why Choose Reason(s)'))
        else:
            self.stdout.write(self.style.WARNING('→ All Why Choose Reasons already exist'))
        
        # Create CTA
        cta, created = TestimonialsPageCTA.objects.get_or_create(
            defaults={
                'badge_icon': 'phone',
                'badge_text': 'Need Help?',
                'headline': 'Ready to Get Started?',
                'description': 'Join 100+ satisfied clients who trust Techlynx Pro for their digital needs.',
                'cta_primary_text': 'Get Your Free Quote',
                'cta_primary_url': '/contact/',
                'cta_primary_icon': 'arrow_forward',
                'cta_secondary_text': 'Call Us Now',
                'cta_secondary_url': 'tel:+1234567890',
                'cta_secondary_icon': 'phone',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Testimonials CTA'))
        else:
            self.stdout.write(self.style.WARNING('→ Testimonials CTA already exists'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Testimonials page population complete!'))
