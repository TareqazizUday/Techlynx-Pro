from django.core.management.base import BaseCommand
from website.models import Partner

class Command(BaseCommand):
    help = 'Create partner companies with logos'

    def handle(self, *args, **kwargs):
        partners_data = [
            {'name': 'Microsoft', 'logo': 'partners/partner1.png', 'order': 1},
            {'name': 'Amazon Web Services', 'logo': 'partners/partner2.png', 'order': 2},
            {'name': 'Google Cloud', 'logo': 'partners/partner3.png', 'order': 3},
            {'name': 'Salesforce', 'logo': 'partners/partner4.png', 'order': 4},
            {'name': 'Oracle', 'logo': 'partners/partner5.png', 'order': 5},
        ]
        
        for partner_data in partners_data:
            partner, created = Partner.objects.get_or_create(
                name=partner_data['name'],
                defaults={
                    'logo': partner_data['logo'],
                    'order': partner_data['order']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {partner.name}'))
            else:
                partner.logo = partner_data['logo']
                partner.order = partner_data['order']
                partner.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Updated: {partner.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(partners_data)} partners added!'))
