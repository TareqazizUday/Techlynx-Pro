from django.core.management.base import BaseCommand
from website.models import CPService
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Add SVG icon images to Content Production services'

    def handle(self, *args, **kwargs):
        icon_mapping = {
            'Blog & Article Writing': 'services/content_production/service_icons/blog_writing.svg',
            'Video Production': 'services/content_production/service_icons/video_production.svg',
            'Graphic Design': 'services/content_production/service_icons/graphic_design.svg',
            'Social Media Content': 'services/content_production/service_icons/social_media.svg',
        }
        
        updated_count = 0
        
        for service_title, icon_path in icon_mapping.items():
            try:
                service = CPService.objects.get(title=service_title)
                full_path = os.path.join(settings.MEDIA_ROOT, icon_path)
                
                if os.path.exists(full_path):
                    service.icon_image = icon_path
                    service.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated {service_title} with icon: {icon_path}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Icon file not found: {full_path}')
                    )
            except CPService.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ Service not found: {service_title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully updated {updated_count} services with SVG icons!')
        )
