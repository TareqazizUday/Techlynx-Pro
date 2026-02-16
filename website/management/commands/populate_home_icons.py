from django.core.management.base import BaseCommand
from website.models import HeroBenefit, Benefit, CompanyStat, Guarantee
import os
from django.conf import settings
from pathlib import Path

class Command(BaseCommand):
    help = 'Create SVG icons for home page elements and populate database'

    def create_svg_icon(self, name, path, icon_type='default'):
        """Create a simple SVG icon file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # SVG templates based on icon type
        svg_templates = {
            'check': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
</svg>''',
            'verified': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
</svg>''',
            'schedule': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
</svg>''',
            'workspace': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M20 6h-2.18c.11-.31.18-.65.18-1 0-1.66-1.34-3-3-3-1.05 0-1.96.54-2.5 1.35l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm11 15H4v-2h16v2zm0-5H4V8h5.08L7 10.83 8.62 12 11 8.76l1-1.36 1 1.36L15.38 12 17 10.83 14.92 8H20v6z"/>
</svg>''',
            'favorite': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
</svg>''',
            'support': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M21 12.22C21 6.73 16.74 3 12 3c-4.69 0-9 3.65-9 9.28-.6.34-1 .98-1 1.72v2c0 1.1.9 2 2 2h1v-6.1c0-3.87 3.13-7 7-7s7 3.13 7 7V19h-8v2h8c1.1 0 2-.9 2-2v-1.22c.59-.31 1-.92 1-1.64v-2.3c0-.7-.41-1.31-1-1.62z"/>
  <circle cx="9" cy="13" r="1"/><circle cx="15" cy="13" r="1"/>
  <path d="M18 11.03C17.52 8.18 15.04 6 12.05 6c-3.03 0-6.29 2.51-6.03 6.45 2.47-1.01 4.33-3.21 4.86-5.89 1.31 2.63 4 4.44 7.12 4.47z"/>
</svg>''',
            'speed': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M20.38 8.57l-1.23 1.85a8 8 0 0 1-.22 7.58H5.07A8 8 0 0 1 15.58 6.85l1.85-1.23A10 10 0 0 0 3.35 19a2 2 0 0 0 1.72 1h13.85a2 2 0 0 0 1.74-1 10 10 0 0 0-.27-10.44zm-9.79 6.84a2 2 0 0 0 2.83 0l5.66-8.49-8.49 5.66a2 2 0 0 0 0 2.83z"/>
</svg>''',
            'analytics': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M5 9.2h3V19H5V9.2zM10.6 5h2.8v14h-2.8V5zm5.6 8H19v6h-2.8v-6z"/>
</svg>''',
            'shield': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
</svg>''',
        }
        
        # Determine which SVG template to use
        svg_content = svg_templates.get(icon_type, svg_templates['check'])
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        
        # Hero Benefits
        self.stdout.write('\n=== Creating Hero Benefit Icons ===')
        hero_benefits = HeroBenefit.objects.all()
        icon_mapping = {
            'check_circle': 'check',
            'schedule': 'schedule',
            'workspace_premium': 'workspace',
            'verified': 'verified',
        }
        
        for benefit in hero_benefits:
            icon_type = icon_mapping.get(benefit.icon, 'check')
            filename = f'{benefit.icon}.svg'
            rel_path = f'hero/benefit_icons/{filename}'
            full_path = os.path.join(media_root, rel_path)
            
            self.create_svg_icon(benefit.icon, full_path, icon_type)
            benefit.icon_image = rel_path
            benefit.save()
            self.stdout.write(self.style.SUCCESS(f'✓ {benefit.title}: {rel_path}'))
        
        # Company Stats
        self.stdout.write('\n=== Creating Company Stat Icons ===')
        stats = CompanyStat.objects.all()
        stat_icon_mapping = {
            'workspace_premium': 'workspace',
            'verified': 'verified',
            'favorite': 'favorite',
            'support_agent': 'support',
        }
        
        for stat in stats:
            icon_type = stat_icon_mapping.get(stat.icon, 'check')
            filename = f'{stat.icon}.svg'
            rel_path = f'stats/icons/{filename}'
            full_path = os.path.join(media_root, rel_path)
            
            self.create_svg_icon(stat.icon, full_path, icon_type)
            stat.icon_image = rel_path
            stat.save()
            self.stdout.write(self.style.SUCCESS(f'✓ {stat.label}: {rel_path}'))
        
        # Benefits
        self.stdout.write('\n=== Creating Benefit Icons ===')
        benefits = Benefit.objects.all()
        benefit_icon_mapping = {
            'verified': 'verified',
            'speed': 'speed',
            'analytics': 'analytics',
        }
        
        for benefit in benefits:
            icon_type = benefit_icon_mapping.get(benefit.icon, 'verified')
            filename = f'{benefit.icon}.svg'
            rel_path = f'benefits/icons/{filename}'
            full_path = os.path.join(media_root, rel_path)
            
            self.create_svg_icon(benefit.icon, full_path, icon_type)
            benefit.icon_image = rel_path
            benefit.save()
            self.stdout.write(self.style.SUCCESS(f'✓ {benefit.title}: {rel_path}'))
        
        # Guarantees
        self.stdout.write('\n=== Creating Guarantee Icons ===')
        guarantees = Guarantee.objects.all()
        
        for guarantee in guarantees:
            icon_type = 'check' if guarantee.icon == 'check_circle' else 'shield'
            filename = f'{guarantee.icon}.svg'
            rel_path = f'guarantees/icons/{filename}'
            full_path = os.path.join(media_root, rel_path)
            
            self.create_svg_icon(guarantee.icon, full_path, icon_type)
            guarantee.icon_image = rel_path
            guarantee.save()
            text_preview = guarantee.text[:40]
            self.stdout.write(self.style.SUCCESS(f'✓ {text_preview}...: {rel_path}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ All home page icons created and populated!'))
