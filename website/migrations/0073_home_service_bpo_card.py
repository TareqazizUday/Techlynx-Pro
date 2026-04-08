from django.db import migrations


def add_bpo_home_service(apps, schema_editor):
    Service = apps.get_model('website', 'Service')
    if Service.objects.filter(detail_page_url='/services/bpo/').exists():
        return
    Service.objects.create(
        title='Business Process Outsourcing (BPO)',
        description=(
            'Outsource support, back office, and data operations with SLAs, documented SOPs, '
            'and QA—secure handoffs and transparent reporting aligned to your volume.'
        ),
        icon='corporate_fare',
        image='services/bpo-outsourcing.jpg',
        detail_page_url='/services/bpo/',
        is_active=True,
        order=0,
    )


def remove_bpo_home_service(apps, schema_editor):
    Service = apps.get_model('website', 'Service')
    Service.objects.filter(detail_page_url='/services/bpo/').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0072_servicedetail_bpo_card_image'),
    ]

    operations = [
        migrations.RunPython(add_bpo_home_service, remove_bpo_home_service),
    ]
