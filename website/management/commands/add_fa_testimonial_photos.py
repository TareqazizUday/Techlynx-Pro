from django.core.management.base import BaseCommand
from website.models import FATestimonial
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Add SVG profile images to Finance & Accounting testimonials'

    def handle(self, *args, **kwargs):
        testimonial_photos = {
            'Robert Chen': '/media/testimonials/finance_accounting/robert_chen.svg',
        }
        
        updated_count = 0
        
        for client_name, photo_url in testimonial_photos.items():
            try:
                testimonial = FATestimonial.objects.get(client_name=client_name)
                
                # Verify the file exists
                media_path = photo_url.replace('/media/', '')
                full_path = os.path.join(settings.MEDIA_ROOT, media_path)
                
                if os.path.exists(full_path):
                    testimonial.client_photo = photo_url
                    testimonial.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated {client_name} with photo: {photo_url}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Photo file not found: {full_path}')
                    )
            except FATestimonial.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ Testimonial not found: {client_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully updated {updated_count} testimonials with SVG photos!')
        )
