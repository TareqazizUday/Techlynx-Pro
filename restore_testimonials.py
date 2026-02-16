#!/usr/bin/env python3
"""
Restore original testimonial images - revert back to original format
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techlynx_project.settings')
django.setup()

from website.models import DigitalMarketingTestimonial

def restore_original_testimonials():
    """Restore testimonials to original SVG format"""
    
    print("🔄 RESTORING ORIGINAL TESTIMONIAL IMAGES...")
    
    # Update Emily Chen to use original SVG
    try:
        emily = DigitalMarketingTestimonial.objects.get(client_name="Emily Chen")
        emily.client_photo = 'testimonials/digital_marketing/emily_chen.svg'
        emily.save()
        print(f"✅ Emily Chen restored to: {emily.client_photo}")
    except DigitalMarketingTestimonial.DoesNotExist:
        print("❌ Emily Chen testimonial not found")
    
    # Update Marcus Thorne to use original SVG  
    try:
        marcus = DigitalMarketingTestimonial.objects.get(client_name="Marcus Thorne")
        marcus.client_photo = 'testimonials/digital_marketing/marcus_thorne.svg'
        marcus.save()
        print(f"✅ Marcus Thorne restored to: {marcus.client_photo}")
    except DigitalMarketingTestimonial.DoesNotExist:
        print("❌ Marcus Thorne testimonial not found")
    
    print("\n🎯 ORIGINAL TESTIMONIAL FORMAT RESTORED!")
    print("📊 Current testimonials:")
    
    testimonials = DigitalMarketingTestimonial.objects.filter(is_active=True).order_by('order')
    for t in testimonials:
        print(f"   - {t.client_name} ({t.client_position})")
        print(f"     Photo: {t.client_photo}")
        print()

if __name__ == '__main__':
    restore_original_testimonials()