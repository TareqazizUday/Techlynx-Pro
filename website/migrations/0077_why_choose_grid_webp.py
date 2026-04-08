"""Replace Why Choose grid with four distinct WebP images (bundled in static, copied to media)."""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db import migrations


def forwards(apps, schema_editor):
    WhyChooseImage = apps.get_model("website", "WhyChooseImage")
    base = Path(settings.BASE_DIR) / "static" / "images" / "services" / "why-choose"
    slots = [
        ("why_grid_1.webp", "Team collaboration at Techlynx Pro"),
        ("why_grid_2.webp", "Modern office teamwork"),
        ("why_grid_3.webp", "Business strategy and presentation"),
        ("why_grid_4.webp", "Data analytics and performance dashboard"),
    ]
    WhyChooseImage.objects.all().delete()
    for order, (fname, alt) in enumerate(slots):
        path = base / fname
        if not path.is_file():
            continue
        obj = WhyChooseImage(order=order, alt_text=alt, is_active=True)
        # Pass filename only — upload_to already adds services/why_choose/
        with open(path, "rb") as f:
            obj.image.save(fname, File(f), save=True)


def backwards(apps, schema_editor):
    WhyChooseImage = apps.get_model("website", "WhyChooseImage")
    WhyChooseImage.objects.filter(image__contains="why_grid_").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0076_virtual_assistance_order_10"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
