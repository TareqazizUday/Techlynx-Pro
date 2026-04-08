from django.db import migrations, models


def seed_bpo_service_detail(apps, schema_editor):
    """
    Create a ServiceDetail card for the main /services/ page if it doesn't exist.
    This links to the dedicated BPO page at /services/bpo/.
    """
    ServiceDetail = apps.get_model('website', 'ServiceDetail')
    exists = ServiceDetail.objects.filter(detail_page_url='/services/bpo/').exists()
    if not exists:
        ServiceDetail.objects.create(
            title='Business Process Outsourcing (BPO)',
            description='SLA-driven outsourced operations for back-office workflows, customer support, and data processing—optimized for speed and accuracy.',
            icon='domain',
            detail_page_url='/services/bpo/',
            order=0,
            is_active=True,
        )


def seed_bpo_defaults(apps, schema_editor):
    """Create default BPO page content including local SVG assets (stored in media/)."""
    BPOHero = apps.get_model('website', 'BPOHero')
    BPOCTA = apps.get_model('website', 'BPOCTA')
    BPOProcessStep = apps.get_model('website', 'BPOProcessStep')
    BPOService = apps.get_model('website', 'BPOService')
    BPOBenefit = apps.get_model('website', 'BPOBenefit')

    if not BPOHero.objects.exists():
        # Store file paths relative to MEDIA_ROOT so images render immediately after upload.
        BPOHero.objects.create(
            is_active=True,
            hero_image='services/bpo/bpo-hero.svg',
        )

    if not BPOCTA.objects.exists():
        BPOCTA.objects.create(is_active=True)

    if not BPOProcessStep.objects.exists():
        BPOProcessStep.objects.bulk_create([
            BPOProcessStep(step_number='01', title='Discovery', description='We map workflows, volume, and SLAs to define success and handoffs.', order=1, is_active=True),
            BPOProcessStep(step_number='02', title='Playbook + QA', description='We document SOPs, implement QA checks, and define reporting cadence.', order=2, is_active=True),
            BPOProcessStep(step_number='03', title='Transition', description='Secure onboarding, tooling access, and pilot execution with fast feedback loops.', order=3, is_active=True),
            BPOProcessStep(step_number='04', title='Scale', description='Expand capacity, optimize performance, and maintain SLAs with continuous improvement.', order=4, is_active=True),
        ])

    if not BPOService.objects.exists():
        BPOService.objects.bulk_create([
            BPOService(icon='support_agent', icon_image='services/bpo/service_icons/customer-support.svg', title='Customer Support Operations', description='Tiered support coverage with QA and SLA reporting.', feature_1='Email, chat & ticket handling', feature_2='Escalation & knowledge base', feature_3='QA sampling + coaching', feature_4='Weekly reporting', order=1, is_active=True),
            BPOService(icon='database', icon_image='services/bpo/service_icons/data-processing.svg', title='Data Processing & Management', description='Accurate data workflows with validation and audit trails.', feature_1='Data entry & enrichment', feature_2='Deduplication & QA', feature_3='Spreadsheet + CRM updates', feature_4='Turnaround SLAs', order=2, is_active=True),
            BPOService(icon='receipt_long', icon_image='services/bpo/service_icons/back-office.svg', title='Back Office & Admin', description='Reliable admin execution for repeatable operational tasks.', feature_1='Document processing', feature_2='Scheduling & coordination', feature_3='Reporting & dashboards', feature_4='Process documentation', order=3, is_active=True),
            BPOService(icon='shield_lock', icon_image='services/bpo/service_icons/compliance.svg', title='Compliance-Ready Workflows', description='Process controls designed to protect your data and brand.', feature_1='Role-based access', feature_2='SOPs + approvals', feature_3='QA + exception handling', feature_4='Secure handoffs', order=4, is_active=True),
        ])

    if not BPOBenefit.objects.exists():
        BPOBenefit.objects.bulk_create([
            BPOBenefit(icon='verified', icon_image='services/bpo/benefit_icons/sla.svg', title='SLA-driven delivery', description='Clear turnaround times and performance targets with transparent reporting.', order=1, is_active=True),
            BPOBenefit(icon='rule_settings', icon_image='services/bpo/benefit_icons/playbook.svg', title='Playbooks + SOPs', description='Documented workflows for consistent execution and easy scaling.', order=2, is_active=True),
            BPOBenefit(icon='manage_search', icon_image='services/bpo/benefit_icons/quality.svg', title='Quality assurance', description='QA checks, sampling, and continuous improvement to protect accuracy.', order=3, is_active=True),
            BPOBenefit(icon='lock', icon_image='services/bpo/benefit_icons/security.svg', title='Security-conscious operations', description='Access controls and secure handoffs aligned with your policies.', order=4, is_active=True),
        ])


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0070_contact_page_dynamic'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPOHero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_icon', models.CharField(default='domain', max_length=50)),
                ('badge_text', models.CharField(default='Operational Excellence', max_length=100)),
                ('headline', models.TextField(default='Business Process Outsourcing (BPO) That Scales With You')),
                ('description', models.TextField(default='Reduce overhead, improve accuracy, and accelerate execution with a dedicated BPO team built around your workflows.')),
                ('cta_primary_text', models.CharField(default='Get a BPO Proposal', max_length=100)),
                ('cta_primary_url', models.CharField(default='/contact/', max_length=200)),
                ('cta_secondary_text', models.CharField(default='View BPO Services', max_length=100)),
                ('cta_secondary_url', models.CharField(default='#bpo-services', max_length=200)),
                ('hero_image', models.ImageField(blank=True, null=True, upload_to='services/bpo/')),
                ('efficiency_gain', models.CharField(default='30-60%', max_length=50)),
                ('sla_coverage', models.CharField(default='24/7', max_length=50)),
                ('qa_accuracy', models.CharField(default='99%+', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'BPO Hero',
                'verbose_name_plural': 'BPO Hero',
            },
        ),
        migrations.CreateModel(
            name='BPOService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(default='support_agent', help_text='Material icon name', max_length=50)),
                ('icon_image', models.FileField(blank=True, help_text='SVG icon file (stored in DB/media)', null=True, upload_to='services/bpo/service_icons/')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('feature_1', models.CharField(blank=True, default='', max_length=200)),
                ('feature_2', models.CharField(blank=True, default='', max_length=200)),
                ('feature_3', models.CharField(blank=True, default='', max_length=200)),
                ('feature_4', models.CharField(blank=True, default='', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'BPO Service',
                'verbose_name_plural': 'BPO Services',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='BPOBenefit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(default='verified', help_text='Material icon name', max_length=50)),
                ('icon_image', models.FileField(blank=True, help_text='SVG icon file (stored in DB/media)', null=True, upload_to='services/bpo/benefit_icons/')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'BPO Benefit',
                'verbose_name_plural': 'BPO Benefits',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='BPOProcessStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.CharField(default='01', max_length=10)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'BPO Process Step',
                'verbose_name_plural': 'BPO Process Steps',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='BPOCTA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(default='Ready to Outsource With Confidence?', max_length=200)),
                ('description', models.TextField(default='Tell us what you want to outsource and we’ll return a workflow-driven plan, SLA, and pricing options.')),
                ('cta_primary_text', models.CharField(default='Talk to a Specialist', max_length=100)),
                ('cta_primary_url', models.CharField(default='/contact/', max_length=200)),
                ('cta_secondary_text', models.CharField(default='See Case Studies', max_length=100)),
                ('cta_secondary_url', models.CharField(default='/case-studies/', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'BPO CTA',
                'verbose_name_plural': 'BPO CTA',
            },
        ),
        migrations.RunPython(seed_bpo_service_detail, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(seed_bpo_defaults, reverse_code=migrations.RunPython.noop),
    ]

