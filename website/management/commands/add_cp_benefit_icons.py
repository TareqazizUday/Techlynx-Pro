from django.core.management.base import BaseCommand
from website.models import CPBenefit
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Add SVG icon images to Content Production benefits'

    def handle(self, *args, **kwargs):
        icon_mapping = {
            '385% Engagement Boost': 'services/content_production/benefit_icons/engagement_boost.svg',
            'Page 1 Rankings': 'services/content_production/benefit_icons/page_rankings.svg',
            '3.2x More Shares': 'services/content_production/benefit_icons/more_shares.svg',
            'Higher Conversions': 'services/content_production/benefit_icons/higher_conversions.svg',
        }
        
        updated_count = 0
        
        for benefit_title, icon_path in icon_mapping.items():
            try:
                benefit = CPBenefit.objects.get(title=benefit_title)
                full_path = os.path.join(settings.MEDIA_ROOT, icon_path)
                
                if os.path.exists(full_path):
                    benefit.icon_image = icon_path
                    benefit.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated {benefit_title} with icon: {icon_path}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Icon file not found: {full_path}')
                    )
            except CPBenefit.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ Benefit not found: {benefit_title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully updated {updated_count} benefits with SVG icons!')
        )
