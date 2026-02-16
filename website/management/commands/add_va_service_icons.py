from django.core.management.base import BaseCommand
from website.models import VAService
import os
from django.conf import settings
from django.core.files import File

class Command(BaseCommand):
    help = 'Add SVG icon images to Virtual Assistance services'

    def handle(self, *args, **kwargs):
        # Create the directory if it doesn't exist
        icon_dir = os.path.join(settings.MEDIA_ROOT, 'services', 'virtual_assistance', 'service_icons')
        os.makedirs(icon_dir, exist_ok=True)
        
        # Icon mapping: service title -> icon filename
        icon_mapping = {
            'Administrative Support': 'admin_support.svg',
            'Customer Service': 'customer_service.svg',
            'Content & Marketing': 'content_marketing.svg',
            'Technical Support': 'technical_support.svg',
            'Data Entry': 'admin_support.svg',  # Fallback
            'Research & Analysis': 'technical_support.svg',  # Fallback
        }
        
        updated_count = 0
        
        for service_title, icon_filename in icon_mapping.items():
            try:
                service = VAService.objects.get(title=service_title)
                icon_path = os.path.join(icon_dir, icon_filename)
                
                if os.path.exists(icon_path):
                    # Open the file and assign it to the service
                    with open(icon_path, 'rb') as f:
                        service.icon_image.save(icon_filename, File(f), save=True)
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[OK] Updated {service_title} with icon: {icon_filename}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'[WARN] Icon file not found: {icon_path}')
                    )
            except VAService.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'[WARN] Service not found: {service_title}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] Error updating {service_title}: {str(e)}')
                )
        
        # Also update any services that don't have icons yet
        services_without_icons = VAService.objects.filter(icon_image__isnull=True, is_active=True)
        for service in services_without_icons:
            # Try to find a matching icon based on title keywords
            icon_filename = None
            title_lower = service.title.lower()
            
            if 'admin' in title_lower or 'administrative' in title_lower:
                icon_filename = 'admin_support.svg'
            elif 'customer' in title_lower or 'service' in title_lower:
                icon_filename = 'customer_service.svg'
            elif 'content' in title_lower or 'marketing' in title_lower:
                icon_filename = 'content_marketing.svg'
            elif 'technical' in title_lower or 'tech' in title_lower or 'support' in title_lower:
                icon_filename = 'technical_support.svg'
            
            if icon_filename:
                icon_path = os.path.join(icon_dir, icon_filename)
                if os.path.exists(icon_path):
                    try:
                        with open(icon_path, 'rb') as f:
                            service.icon_image.save(icon_filename, File(f), save=True)
                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'[OK] Updated {service.title} with icon: {icon_filename}')
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'[ERROR] Error updating {service.title}: {str(e)}')
                        )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n[SUCCESS] Successfully updated {updated_count} services with SVG icons!')
        )

