from django.core.management.base import BaseCommand
from website.models import CPTechnology

class Command(BaseCommand):
    help = 'Populate Content Production Technologies'

    def handle(self, *args, **kwargs):
        technologies = [
            {
                'title': 'Design Suite',
                'icon': 'draw',
                'icon_image': 'services/content_production/tech_icons/design_suite.svg',
                'description': 'Adobe Creative Cloud, Figma, and Canva for stunning visual content.',
                'order': 1,
            },
            {
                'title': 'Video Editing',
                'icon': 'movie_edit',
                'icon_image': 'services/content_production/tech_icons/video_editing.svg',
                'description': 'Adobe Premiere Pro, Final Cut Pro, and DaVinci Resolve for professional videos.',
                'order': 2,
            },
            {
                'title': 'Content Management',
                'icon': 'edit_note',
                'icon_image': 'services/content_production/tech_icons/content_management.svg',
                'description': 'WordPress, HubSpot, and ContentStack for seamless publishing.',
                'order': 3,
            },
        ]

        CPTechnology.objects.all().delete()
        
        for tech_data in technologies:
            tech = CPTechnology.objects.create(**tech_data)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created: {tech.title}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully populated {len(technologies)} technologies!')
        )
