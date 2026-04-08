from django.db import migrations


def va_order_10(apps, schema_editor):
    Service = apps.get_model('website', 'Service')
    ServiceDetail = apps.get_model('website', 'ServiceDetail')
    Service.objects.filter(title='Virtual Assistance').update(order=10)
    ServiceDetail.objects.filter(title='Virtual Assistance').update(order=10)


def va_restore(apps, schema_editor):
    Service = apps.get_model('website', 'Service')
    ServiceDetail = apps.get_model('website', 'ServiceDetail')
    Service.objects.filter(title='Virtual Assistance').update(order=9)
    ServiceDetail.objects.filter(title='Virtual Assistance').update(order=7)


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0075_servicedetail_bpo_first_row'),
    ]

    operations = [
        migrations.RunPython(va_order_10, va_restore),
    ]
