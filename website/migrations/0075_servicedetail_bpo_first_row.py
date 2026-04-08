from django.db import migrations


def bpo_first_row(apps, schema_editor):
    ServiceDetail = apps.get_model('website', 'ServiceDetail')
    ServiceDetail.objects.filter(detail_page_url='/services/bpo/').update(order=0)


def bpo_restore_tail(apps, schema_editor):
    ServiceDetail = apps.get_model('website', 'ServiceDetail')
    ServiceDetail.objects.filter(detail_page_url='/services/bpo/').update(order=999)


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0074_bpo_home_card_first_row'),
    ]

    operations = [
        migrations.RunPython(bpo_first_row, bpo_restore_tail),
    ]
