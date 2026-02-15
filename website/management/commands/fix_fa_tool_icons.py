from django.core.management.base import BaseCommand
from website.models import FATool
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Fix FA tool icons by mapping them to the correct SVG files'

    def handle(self, *args, **kwargs):
        # Mapping of tool names to their SVG files
        icon_mapping = {
            'QuickBooks': 'bookkeeping_accounting.svg',
            'ADP': 'adp.svg',
            'NetSuite': 'netsuite.svg',
            'Xero': 'xero.svg',
            'Sage': 'sage.svg',
            'Gusto': 'gusto.svg',
        }

        media_path = 'media/services/finance_accounting/tool_icons/'
        
        for tool_name, svg_filename in icon_mapping.items():
            try:
                tool = FATool.objects.get(name=tool_name)
                icon_path = f'services/finance_accounting/tool_icons/{svg_filename}'
                
                # Update the icon_image field
                tool.icon_image = icon_path
                tool.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated {tool_name} with {svg_filename}')
                )
            except FATool.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Tool not found: {tool_name}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error updating {tool_name}: {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS('\n✓ All FA tool icons have been updated!'))
