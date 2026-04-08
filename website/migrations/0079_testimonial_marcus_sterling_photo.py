from django.db import migrations


def set_photo(apps, schema_editor):
    Testimonial = apps.get_model("website", "Testimonial")
    Testimonial.objects.filter(
        client_name="Marcus Sterling", client_company="Sterling Fintech"
    ).update(client_photo="testimonials/marcus_sterling.jpg")


def clear_photo(apps, schema_editor):
    Testimonial = apps.get_model("website", "Testimonial")
    Testimonial.objects.filter(
        client_name="Marcus Sterling", client_company="Sterling Fintech"
    ).update(client_photo=None)


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0078_fix_why_choose_image_paths"),
    ]

    operations = [
        migrations.RunPython(set_photo, clear_photo),
    ]
