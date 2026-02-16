from django.core.management.base import BaseCommand
from website.models import AboutPageTimeline


class Command(BaseCommand):
    help = 'Fix timeline order to start from 2018'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fixing timeline order...\n')
        
        # Delete any items with year 2025
        items_2025 = AboutPageTimeline.objects.filter(year__icontains='2025')
        if items_2025.exists():
            count = items_2025.count()
            items_2025.delete()
            self.stdout.write(self.style.WARNING(f'  [!] Deleted {count} item(s) with year 2025'))
        
        # Reset all orders to 0 first
        AboutPageTimeline.objects.all().update(order=0)
        
        # Set correct order starting from 2018
        timeline_data = [
            {'year': '2018', 'order': 1},
            {'year': '2020', 'order': 2},
            {'year': '2022', 'order': 3},
            {'year': 'Present', 'order': 4},
        ]
        
        for data in timeline_data:
            updated = AboutPageTimeline.objects.filter(year=data['year']).update(order=data['order'])
            if updated > 0:
                self.stdout.write(self.style.SUCCESS(f"  [OK] Set {data['year']} to order {data['order']}"))
        
        # Verify final order
        self.stdout.write('\nFinal timeline order:')
        items = AboutPageTimeline.objects.filter(is_active=True).order_by('order')
        for item in items:
            self.stdout.write(f"  {item.order}. {item.year} - {item.title}")
        
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Timeline order fixed! 2018 is now first.'))

