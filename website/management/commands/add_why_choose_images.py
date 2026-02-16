from django.core.management.base import BaseCommand
from website.models import WhyChooseImage
import os
from django.conf import settings
from django.core.files import File


class Command(BaseCommand):
    help = 'Add Why Choose images from media folder to database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding Why Choose images...\n')
        
        # Image files in the media folder
        image_files = [
            'why_choose_1.jpg',
            'why_choose_2.jpg',
            'why_choose_3.jpg',
            'why_choose_4.jpg',
        ]
        
        # Base path for images
        base_path = 'services/why_choose'
        
        # Clear existing images if needed (optional - comment out if you want to keep existing)
        # WhyChooseImage.objects.all().delete()
        # self.stdout.write(self.style.WARNING('Cleared existing Why Choose images\n'))
        
        for index, image_file in enumerate(image_files, start=1):
            image_path = os.path.join(base_path, image_file)
            full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            
            # Check if image exists
            if not os.path.exists(full_path):
                self.stdout.write(self.style.WARNING(f'[X] Image not found: {full_path}'))
                continue
            
            # Check if image already exists in database
            existing = WhyChooseImage.objects.filter(image=image_path).first()
            if existing:
                self.stdout.write(self.style.WARNING(f'[!] Image already exists: {image_file} (skipping)'))
                continue
            
            # Create new WhyChooseImage entry
            try:
                with open(full_path, 'rb') as f:
                    why_choose_image = WhyChooseImage(
                        alt_text=f'Why Choose Techlynx Pro - Image {index}',
                        order=index,
                        is_active=True
                    )
                    why_choose_image.image.save(
                        image_file,
                        File(f),
                        save=True
                    )
                    self.stdout.write(self.style.SUCCESS(f'[OK] Added: {image_file} (Order: {index})'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] Error adding {image_file}: {str(e)}'))
        
        # Show summary
        total_images = WhyChooseImage.objects.filter(is_active=True).count()
        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Total active Why Choose images: {total_images}'))
        self.stdout.write(self.style.SUCCESS('You can now manage these images from the admin panel!'))

