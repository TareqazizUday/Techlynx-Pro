from django.core.management.base import BaseCommand
from website.models import CaseStudiesPageCTA


class Command(BaseCommand):
    help = 'Populate Case Studies Page CTA content'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating Case Studies Page CTA...')
        
        # Clear existing CTAs
        CaseStudiesPageCTA.objects.all().delete()
        
        # Create CTA
        cta = CaseStudiesPageCTA.objects.create(
            headline='Ready for Similar Results?',
            description="Let's discuss how we can help transform your business with proven strategies and solutions.",
            primary_button_text='Start Your Project',
            primary_button_url='/contact/',
            secondary_button_text='View More Case Studies',
            secondary_button_url='/case-studies/',
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created: {cta.headline}'))
        self.stdout.write(self.style.SUCCESS('\n✨ Case Studies Page CTA created successfully!'))
