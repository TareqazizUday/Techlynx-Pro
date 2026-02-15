from django.core.management.base import BaseCommand
from website.models import (
    AITestimonial, DigitalMarketingTestimonial, AppDevTestimonial,
    SEOAuditTestimonial, PMTestimonial, FATestimonial, CPTestimonial
)


class Command(BaseCommand):
    help = 'Add sample testimonials for all services'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding sample testimonials...')
        
        # AI Solutions Testimonials
        ai_testimonials = [
            {
                'client_name': 'Sarah Mitchell',
                'client_position': 'CEO, TechVentures Inc.',
                'testimonial_text': 'Techlynx Pro transformed our business with their AI solutions. We saw a 45% increase in operational efficiency within just 3 months. Their team is incredibly knowledgeable and responsive.',
                'order': 1,
                'is_active': True
            },
            {
                'client_name': 'James Rodriguez',
                'client_position': 'CTO, InnovateHub',
                'testimonial_text': 'The AI chatbot they built for us handles 80% of customer inquiries automatically. Our support team can now focus on complex issues. Absolutely game-changing!',
                'order': 2,
                'is_active': True
            }
        ]
        
        for data in ai_testimonials:
            AITestimonial.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created AI testimonial: {data["client_name"]}'))
        
        # Digital Marketing Testimonials
        marketing_testimonials = [
            {
                'client_name': 'Emily Chen',
                'client_position': 'Marketing Director, RetailPro',
                'testimonial_text': 'Our organic traffic increased by 300% in 6 months! Their SEO and content marketing strategy is phenomenal. The ROI has been outstanding.',
                'order': 1,
                'is_active': True
            },
            {
                'client_name': 'Michael Brown',
                'client_position': 'Founder, EcoProducts',
                'testimonial_text': 'Best marketing investment we ever made. They helped us reduce ad spend by 40% while increasing conversions by 150%. Highly recommended!',
                'order': 2,
                'is_active': True
            }
        ]
        
        for data in marketing_testimonials:
            DigitalMarketingTestimonial.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created Marketing testimonial: {data["client_name"]}'))
        
        # App Development Testimonials
        app_testimonials = [
            {
                'client_name': 'Lisa Anderson',
                'client_position': 'Product Manager, HealthTech Solutions',
                'testimonial_text': 'They delivered our mobile app ahead of schedule and under budget. The quality is exceptional, and our users love it. 4.8 stars on both app stores!',
                'order': 1,
                'is_active': True
            },
            {
                'client_name': 'David Wilson',
                'client_position': 'CEO, FitLife App',
                'testimonial_text': 'Professional, communicative, and talented. They took our vision and created something even better than we imagined. Our app has over 50K downloads now!',
                'order': 2,
                'is_active': True
            }
        ]
        
        for data in app_testimonials:
            AppDevTestimonial.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created App Dev testimonial: {data["client_name"]}'))
        
        # SEO Audit Testimonials
        seo_testimonials = [
            {
                'client_name': 'Robert Thompson',
                'client_position': 'Owner, Local Services Co.',
                'testimonial_text': 'Their SEO audit revealed issues we never knew existed. After implementing their recommendations, we jumped from page 5 to page 1 for our main keywords!',
                'order': 1,
                'is_active': True
            }
        ]
        
        for data in seo_testimonials:
            SEOAuditTestimonial.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created SEO testimonial: {data["client_name"]}'))
        
        # Project Management Testimonials
        pm_testimonials = [
            {
                'client_name': 'Jennifer Lee',
                'client_position': 'Operations Director, BuildCorp',
                'testimonial_text': 'Project delivery time reduced by 35% after implementing their PM solutions. Communication and collaboration have never been better.',
                'order': 1,
                'is_active': True
            }
        ]
        
        for data in pm_testimonials:
            PMTestimonial.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created PM testimonial: {data["client_name"]}'))
        
        # Finance & Accounting Testimonials
        fa_testimonials = [
            {
                'client_name': 'Thomas Martinez',
                'client_position': 'CFO, Growth Ventures',
                'testimonial_text': 'Their finance automation solutions saved us 20 hours per week on bookkeeping. Accuracy has improved and our team is more productive.',
                'order': 1,
                'is_active': True
            }
        ]
        
        for data in fa_testimonials:
            FATestimonial.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created FA testimonial: {data["client_name"]}'))
        
        # Content Production Testimonials
        cp_testimonials = [
            {
                'client_name': 'Amanda White',
                'client_position': 'Content Manager, MediaHub',
                'testimonial_text': 'Content quality and output increased dramatically. They streamlined our entire production workflow. Our audience engagement is up 200%!',
                'order': 1,
                'is_active': True
            }
        ]
        
        for data in cp_testimonials:
            CPTestimonial.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created CP testimonial: {data["client_name"]}'))
        
        self.stdout.write(self.style.SUCCESS('\n✨ Sample testimonials added successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Total: {sum([len(ai_testimonials), len(marketing_testimonials), len(app_testimonials), len(seo_testimonials), len(pm_testimonials), len(fa_testimonials), len(cp_testimonials)])} testimonials'))
