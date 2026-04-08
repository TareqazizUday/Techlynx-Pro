"""Fix doubled upload_to path on WhyChooseImage; re-seed from static; remove nested junk folder."""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db import migrations


def forwards(apps, schema_editor):
    WhyChooseImage = apps.get_model("website", "WhyChooseImage")
    media_root = Path(settings.MEDIA_ROOT)
    nested = media_root / "services" / "why_choose" / "services"
    if nested.exists():
        shutil.rmtree(nested, ignore_errors=True)

    static_base = Path(settings.BASE_DIR) / "static" / "images" / "services" / "why-choose"
    slots = [
        ("why_grid_1.webp", "Team collaboration at Techlynx Pro"),
        ("why_grid_2.webp", "Modern office teamwork"),
        ("why_grid_3.webp", "Business strategy and presentation"),
        ("why_grid_4.webp", "Data analytics and performance dashboard"),
    ]

    WhyChooseImage.objects.all().delete()
    for order, (fname, alt) in enumerate(slots):
        path = static_base / fname
        if not path.is_file():
            continue
        obj = WhyChooseImage(order=order, alt_text=alt, is_active=True)
        with open(path, "rb") as f:
            obj.image.save(fname, File(f), save=True)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0077_why_choose_grid_webp"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
