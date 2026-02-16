from django.core.management.base import BaseCommand
from website.models import Service, ServiceDetail

class Command(BaseCommand):
    help = 'Copy images from Service to ServiceDetail model'

    def handle(self, *args, **kwargs):
        services = Service.objects.all()
        
        for service in services:
            try:
                # Find matching ServiceDetail by title
                service_detail = ServiceDetail.objects.get(title=service.title)
                
                if service.image and not service_detail.image:
                    service_detail.image = service.image
                    service_detail.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'✓ {service.title}: {service.image}'
                    ))
                elif service_detail.image:
                    self.stdout.write(self.style.WARNING(
                        f'⊙ {service.title}: Already has image'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'✗ {service.title}: No image in Service model'
                    ))
                    
            except ServiceDetail.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f'✗ {service.title}: ServiceDetail not found'
                ))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Image sync completed!'))
