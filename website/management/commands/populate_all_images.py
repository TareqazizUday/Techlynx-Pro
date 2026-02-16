from django.core.management.base import BaseCommand
from website.models import Partner, Service
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate all missing images from media folder'

    def handle(self, *args, **kwargs):
        # Populate Partner Logos
        self.stdout.write('Populating Partner Logos...')
        partners = Partner.objects.all()
        for i, partner in enumerate(partners, start=1):
            if not partner.logo:
                logo_path = f'partners/partner{i}.png'
                full_path = os.path.join(settings.MEDIA_ROOT, logo_path)
                if os.path.exists(full_path):
                    partner.logo = logo_path
                    partner.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ {partner.name}: {logo_path}'))
        
        # Populate Service Images
        self.stdout.write('\nPopulating Service Images...')
        service_images = {
            'AI Solutions': 'services/ai-solutions_Sm4KGCl.jpg',
            'Web Development': 'services/web-development_8ihFnF4.jpg',
            'Digital Marketing': 'services/digital-marketing_8PPCP5a.jpg',
            'App Development': 'services/app-development_LgLOO2v.jpg',
            'SEO Audit': 'services/seo-audit_cwZznba.jpg',
            'Finance & Accounting': 'services/finance-accounting_2HYTx0j.jpg',
            'Project Management': 'services/project-management_9eVoEHy.jpg',
            'Virtual Assistance': 'services/virtual-assistance.jpg',
            'Content Production': 'services/content-production_Ydlk6M4.jpg',
        }
        
        for service_title, image_path in service_images.items():
            try:
                service = Service.objects.get(title=service_title)
                full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                if os.path.exists(full_path) and not service.image:
                    service.image = image_path
                    service.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ {service_title}: {image_path}'))
            except Service.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'✗ Service not found: {service_title}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ All images populated successfully!'))
