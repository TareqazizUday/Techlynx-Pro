from django.db import migrations


def bpo_first_row(apps, schema_editor):
    Service = apps.get_model('website', 'Service')
    Service.objects.filter(detail_page_url='/services/bpo/').update(order=0)


def bpo_restore_order(apps, schema_editor):
    Service = apps.get_model('website', 'Service')
    Service.objects.filter(detail_page_url='/services/bpo/').update(order=10)


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0073_home_service_bpo_card'),
    ]

    operations = [
        migrations.RunPython(bpo_first_row, bpo_restore_order),
    ]
