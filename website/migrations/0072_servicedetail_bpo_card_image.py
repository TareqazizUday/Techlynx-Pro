from django.db import migrations


def set_bpo_service_card_image(apps, schema_editor):
    """
    Match other service cards (e.g. AI Solutions uses ServiceDetail.image → media/services/*.jpg).
    """
    ServiceDetail = apps.get_model('website', 'ServiceDetail')
    ServiceDetail.objects.filter(detail_page_url='/services/bpo/').update(
        image='services/bpo-outsourcing.jpg',
    )


def clear_bpo_service_card_image(apps, schema_editor):
    ServiceDetail = apps.get_model('website', 'ServiceDetail')
    ServiceDetail.objects.filter(detail_page_url='/services/bpo/').update(image=None)


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0071_bpo_service_page'),
    ]

    operations = [
        migrations.RunPython(set_bpo_service_card_image, clear_bpo_service_card_image),
    ]
