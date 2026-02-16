from django.core.management.base import BaseCommand
from website.models import CPTestimonial
from django.core.files.base import ContentFile
import base64

class Command(BaseCommand):
    help = 'Add placeholder profile images to Content Production testimonials'

    def handle(self, *args, **kwargs):
        # Simple SVG avatars for Sarah and Marcus
        sarah_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
            <rect fill="#e0f2fe" width="200" height="200"/>
            <circle cx="100" cy="80" r="40" fill="#0284c7"/>
            <path d="M50 200 Q100 150 150 200" fill="#0284c7"/>
            <text x="100" y="100" font-family="Arial" font-size="60" fill="#fff" text-anchor="middle" dominant-baseline="middle">S</text>
        </svg>'''
        
        marcus_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
            <rect fill="#ddd6fe" width="200" height="200"/>
            <circle cx="100" cy="80" r="40" fill="#7c3aed"/>
            <path d="M50 200 Q100 150 150 200" fill="#7c3aed"/>
            <text x="100" y="100" font-family="Arial" font-size="60" fill="#fff" text-anchor="middle" dominant-baseline="middle">M</text>
        </svg>'''
        
        testimonials = {
            'Sarah Thompson': ('sarah_thompson.svg', sarah_svg),
            'Marcus Bennett': ('marcus_bennett.svg', marcus_svg),
        }
        
        updated_count = 0
        
        for client_name, (filename, svg_content) in testimonials.items():
            try:
                testimonial = CPTestimonial.objects.get(client_name=client_name)
                
                # Save SVG file directly to the testimonial
                testimonial.client_photo.save(
                    filename,
                    ContentFile(svg_content.encode('utf-8')),
                    save=True
                )
                
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated {client_name} with photo: {filename}')
                )
            except CPTestimonial.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'! Testimonial not found: {client_name}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error updating {client_name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Updated {updated_count} testimonial(s) with photos')
        )
