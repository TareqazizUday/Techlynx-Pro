from django.core.management.base import BaseCommand
from website.models import (
    FAHero, FAService, FATool, FAProcess, FABenefit, FATestimonial, FACTA
)


class Command(BaseCommand):
    help = 'Populate Finance & Accounting page with initial content'

    def handle(self, *args, **options):
        self.stdout.write('Populating Finance & Accounting content...')

        # Create Hero Section
        hero, created = FAHero.objects.get_or_create(
            defaults={
                'badge_icon': 'account_balance',
                'badge_text': 'Strategic Financial Management',
                'headline': 'Expert <span class="text-primary">Finance & Accounting</span> Solutions',
                'description': 'Professional bookkeeping, financial reporting, tax compliance, and CFO services that give you clarity and control over your business finances. Focus on growth while we handle the numbers.',
                'cta_primary_text': 'Get Financial Consultation',
                'cta_primary_url': '/contact/',
                'cta_secondary_text': 'View Case Studies',
                'cta_secondary_url': '/case-studies/',
                'cost_savings_percentage': 42,
                'time_saved_monthly': 280,
                'error_rate': 0.02,
                'compliance_guarantee': '100% Compliance Guarantee',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created FA Hero section')

        # Create Services
        services_data = [
            {
                'title': 'Bookkeeping & Accounting',
                'description': 'Daily transaction recording, account reconciliation, and financial record maintenance.',
                'icon': 'receipt_long',
                'icon_image': 'services/finance_accounting/service_icons/bookkeeping_accounting.svg',
                'feature_1': 'Transaction Processing',
                'feature_2': 'Bank Reconciliation',
                'feature_3': 'General Ledger Management',
                'feature_4': 'Account Monitoring',
                'color_scheme': 'blue',
                'order': 1,
            },
            {
                'title': 'Financial Reporting',
                'description': 'Comprehensive financial statements, P&L, balance sheets, and cash flow analysis.',
                'icon': 'assessment',
                'icon_image': 'services/finance_accounting/service_icons/financial_reporting.svg',
                'feature_1': 'Monthly Statements',
                'feature_2': 'KPI Dashboards',
                'feature_3': 'Performance Analytics',
                'feature_4': 'Variance Analysis',
                'color_scheme': 'green',
                'order': 2,
            },
            {
                'title': 'Tax Preparation & Planning',
                'description': 'Strategic tax planning, preparation, filing, and compliance with IRS regulations.',
                'icon': 'gavel',
                'icon_image': 'services/finance_accounting/service_icons/tax_preparation.svg',
                'feature_1': 'Tax Optimization',
                'feature_2': 'IRS Compliance',
                'feature_3': 'Strategic Planning',
                'feature_4': 'Filing Support',
                'color_scheme': 'purple',
                'order': 3,
            },
            {
                'title': 'Virtual CFO Services',
                'description': 'Strategic financial leadership, forecasting, budgeting, and business advisory.',
                'icon': 'business_center',
                'icon_image': 'services/finance_accounting/service_icons/virtual_cfo.svg',
                'feature_1': 'Financial Strategy',
                'feature_2': 'Budget Planning',
                'feature_3': 'Cash Flow Management',
                'feature_4': 'Investment Advisory',
                'color_scheme': 'orange',
                'order': 4,
            },
        ]

        for service_data in services_data:
            service, created = FAService.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'  ✓ Created FA Service: {service.title}')

        # Create Tools
        tools_data = [
            {
                'name': 'QuickBooks',
                'category': 'Cloud Accounting Platforms',
                'description': 'QuickBooks Online, Xero, and FreshBooks for seamless financial management.',
                'icon': 'calculate',
                'icon_image': 'services/finance_accounting/tool_icons/cloud_accounting.svg',
                'color_scheme': 'blue',
                'order': 1,
            },
            {
                'name': 'ADP',
                'category': 'Payroll & HR Integration',
                'description': 'ADP, Gusto, and Paychex for comprehensive payroll processing.',
                'icon': 'paid',
                'icon_image': 'services/finance_accounting/tool_icons/payroll_hr.svg',
                'color_scheme': 'green',
                'order': 2,
            },
            {
                'name': 'NetSuite',
                'category': 'ERP & Financial Systems',
                'description': 'NetSuite, Sage, and SAP integration for enterprise finance management.',
                'icon': 'currency_exchange',
                'icon_image': 'services/finance_accounting/tool_icons/erp_systems.svg',
                'color_scheme': 'purple',
                'order': 3,
            },
            {
                'name': 'Xero',
                'category': 'Cloud Accounting Platforms',
                'description': 'Advanced cloud-based accounting software for small to medium businesses.',
                'icon': 'calculate',
                'color_scheme': 'blue',
                'order': 4,
            },
            {
                'name': 'Sage',
                'category': 'ERP & Financial Systems',
                'description': 'Comprehensive business management solutions for growing companies.',
                'icon': 'currency_exchange',
                'color_scheme': 'purple',
                'order': 5,
            },
            {
                'name': 'Gusto',
                'category': 'Payroll & HR Integration',
                'description': 'Modern payroll and HR platform for streamlined employee management.',
                'icon': 'paid',
                'color_scheme': 'green',
                'order': 6,
            },
        ]

        for tool_data in tools_data:
            tool, created = FATool.objects.get_or_create(
                name=tool_data['name'],
                defaults=tool_data
            )
            if created:
                self.stdout.write(f'  ✓ Created FA Tool: {tool.name}')

        # Create Process Steps
        process_data = [
            {
                'step_number': 1,
                'title': 'Account Setup',
                'description': 'Chart of accounts creation, system integration, and clean historical data migration.',
                'order': 1,
            },
            {
                'step_number': 2,
                'title': 'Daily Operations',
                'description': 'Transaction recording, invoice processing, expense tracking, and payroll management.',
                'order': 2,
            },
            {
                'step_number': 3,
                'title': 'Monthly Close',
                'description': 'Account reconciliation, financial statements, variance analysis, and reporting.',
                'order': 3,
            },
            {
                'step_number': 4,
                'title': 'Strategic Advisory',
                'description': 'Business insights, forecasting, tax planning, and growth strategy recommendations.',
                'order': 4,
            },
        ]

        for process_data_item in process_data:
            process, created = FAProcess.objects.get_or_create(
                step_number=process_data_item['step_number'],
                defaults=process_data_item
            )
            if created:
                self.stdout.write(f'  ✓ Created FA Process Step {process.step_number}: {process.title}')

        # Create Benefits
        benefits_data = [
            {
                'title': '42% Cost Reduction',
                'description': 'Lower overhead vs hiring full-time accounting staff.',
                'metric': '42% Cost Reduction',
                'icon': 'trending_down',
                'icon_image': 'services/finance_accounting/benefit_icons/cost_reduction.svg',
                'order': 1,
            },
            {
                'title': '280 Hours Saved',
                'description': 'Monthly time savings to focus on core business activities.',
                'metric': '280 Hours Saved',
                'icon': 'speed',
                'icon_image': 'services/finance_accounting/benefit_icons/time_saved.svg',
                'order': 2,
            },
            {
                'title': '100% Compliance',
                'description': 'Stay compliant with IRS, GAAP, and industry regulations.',
                'metric': '100% Compliance',
                'icon': 'shield',
                'icon_image': 'services/finance_accounting/benefit_icons/compliance.svg',
                'order': 3,
            },
            {
                'title': '99.98% Accuracy',
                'description': 'Error-free bookkeeping with certified professionals.',
                'metric': '99.98% Accuracy',
                'icon': 'verified',
                'icon_image': 'services/finance_accounting/benefit_icons/accuracy.svg',
                'order': 4,
            },
        ]

        for benefit_data in benefits_data:
            benefit, created = FABenefit.objects.get_or_create(
                title=benefit_data['title'],
                defaults=benefit_data
            )
            if created:
                self.stdout.write(f'  ✓ Created FA Benefit: {benefit.title}')

        # Create Testimonials
        testimonials_data = [
            {
                'client_name': 'Robert Chen',
                'client_position': 'CEO',
                'client_company': 'TechStart Inc',
                'testimonial_text': 'Switching to their finance team saved us $8K/month and gave us real-time financial visibility. Best decision we made for our startup.',
                'order': 1,
            },
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = FATestimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'  ✓ Created FA Testimonial: {testimonial.client_name}')

        # Create CTA Section
        cta, created = FACTA.objects.get_or_create(
            defaults={
                'headline': 'Ready to Optimize Your Finances?',
                'description': 'Get expert financial management that saves time, reduces costs, and provides the insights you need to grow your business confidently.',
                'cta_primary_text': 'Get Free Financial Review',
                'cta_primary_url': '/contact/',
                'cta_secondary_text': 'View Pricing Options',
                'cta_secondary_url': '/contact/',
                'guarantee_text': 'CPA-certified accountants with 20+ years of experience.',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created FA CTA section')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated Finance & Accounting content!')
        )