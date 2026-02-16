from django.core.management.base import BaseCommand
from website.models import FATestimonial

class Command(BaseCommand):
    help = 'Remove Amanda Williams testimonial from Finance & Accounting page'

    def handle(self, *args, **kwargs):
        try:
            testimonial = FATestimonial.objects.get(client_name='Amanda Williams')
            testimonial.delete()
            self.stdout.write(
                self.style.SUCCESS('✓ Successfully removed Amanda Williams testimonial')
            )
        except FATestimonial.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('! Amanda Williams testimonial not found in database')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error removing testimonial: {str(e)}')
            )
