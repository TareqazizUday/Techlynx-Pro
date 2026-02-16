from django.core.management.base import BaseCommand
from website.models import ServicesPageHero
import os
from django.conf import settings
from django.core.files import File


class Command(BaseCommand):
    help = 'Add Services Hero image from media folder to database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding Services Hero image...\n')
        
        # Image file path
        image_file = 'services_hero.jpg'
        base_path = 'services/hero'
        image_path = os.path.join(base_path, image_file)
        full_path = os.path.join(settings.MEDIA_ROOT, image_path)
        
        # Check if image exists
        if not os.path.exists(full_path):
            self.stdout.write(self.style.ERROR(f'[ERROR] Image not found: {full_path}'))
            self.stdout.write(self.style.WARNING('Please make sure the image is at: media/services/hero/services_hero.jpg'))
            return
        
        # Get or create ServicesPageHero (singleton)
        hero, created = ServicesPageHero.objects.get_or_create(
            defaults={
                'badge_text': 'Trusted US-Based Agency',
                'headline': 'Scalable IT & Digital Marketing Solutions',
                'subheadline': 'High-performance expertise to help your business dominate the digital landscape through SEO-first methodologies.',
                'cta_primary_text': 'View Our Services',
                'cta_primary_url': '#services',
                'cta_secondary_text': 'Talk to an Expert',
                'cta_secondary_url': '/contact',
            }
        )
        
        # Check if image already exists
        if hero.hero_image and hero.hero_image.name == image_path:
            self.stdout.write(self.style.WARNING(f'[!] Image already exists: {image_file}'))
            self.stdout.write(self.style.SUCCESS('You can update it from the admin panel if needed.'))
            return
        
        # Add image to hero
        try:
            with open(full_path, 'rb') as f:
                hero.hero_image.save(
                    image_file,
                    File(f),
                    save=True
                )
                self.stdout.write(self.style.SUCCESS(f'[OK] Added hero image: {image_file}'))
                self.stdout.write(self.style.SUCCESS(f'[OK] Hero section: {hero.headline}'))
                self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Services hero image added successfully!'))
                self.stdout.write(self.style.SUCCESS('You can now manage this image from the admin panel!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'[ERROR] Error adding image: {str(e)}'))

