from django.core.management.base import BaseCommand
from website.models import SEOAuditHero, SEOAuditService, SEOAuditTool, SEOAuditToolLogo, SEOAuditBenefit
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Populate initial data for SEO Audit page (Hero, Services, Tools, and Logos)'

    def handle(self, *args, **kwargs):
        # Create or update Hero section
        hero, created = SEOAuditHero.objects.get_or_create(
            defaults={
                'badge_icon': 'search',
                'badge_text': 'Data-Driven SEO Strategy',
                'headline': 'Dominate Search Rankings with <span class="text-primary">Expert SEO</span> Audits',
                'description': 'Comprehensive technical SEO audits that uncover hidden issues and unlock organic growth. Get actionable insights to outrank competitors and drive qualified traffic that converts.',
                'cta_primary_text': 'Get Free SEO Audit',
                'cta_primary_url': '/contact/',
                'cta_secondary_text': 'View SEO Results',
                'cta_secondary_url': '/case-studies/',
                'traffic_growth': 475,
                'domain_authority': 68,
                'keywords_ranked': 1247,
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Created SEO Audit Hero'))
        else:
            self.stdout.write(self.style.WARNING('[INFO] SEO Audit Hero already exists, skipping...'))

        # Create Services
        services_data = [
            {
                'title': 'Technical SEO Audit',
                'icon': 'search',
                'description': 'Comprehensive analysis of site structure, crawlability, indexing, and technical performance issues.',
                'feature_1': 'Site speed optimization',
                'feature_2': 'Mobile responsiveness check',
                'order': 1,
                'icon_file': 'technical_seo_audit.svg',
            },
            {
                'title': 'On-Page SEO Analysis',
                'icon': 'description',
                'description': 'Detailed review of content quality, keyword optimization, meta tags, and internal linking structure.',
                'feature_1': 'Content optimization',
                'feature_2': 'Meta tag improvements',
                'order': 2,
                'icon_file': 'on_page_seo_analysis.svg',
            },
            {
                'title': 'Backlink Profile Audit',
                'icon': 'link',
                'description': 'Complete analysis of your backlink profile, identifying toxic links and opportunities for quality link building.',
                'feature_1': 'Link quality assessment',
                'feature_2': 'Toxic link removal',
                'order': 3,
                'icon_file': 'backlink_profile_audit.svg',
            },
            {
                'title': 'Competitor Analysis',
                'icon': 'analytics',
                'description': 'In-depth competitor research to identify ranking opportunities and competitive gaps in your SEO strategy.',
                'feature_1': 'Keyword gap analysis',
                'feature_2': 'Content strategy insights',
                'order': 4,
                'icon_file': 'competitor_analysis.svg',
            },
        ]

        created_count = 0
        updated_count = 0

        for service_data in services_data:
            icon_file = service_data.pop('icon_file')
            service, created = SEOAuditService.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    **service_data,
                    'is_active': True,
                }
            )
            
            # Try to assign icon image if file exists
            icon_path = f'services/seo_audit/service_icons/{icon_file}'
            full_path = os.path.join(settings.MEDIA_ROOT, icon_path)
            
            if os.path.exists(full_path) and not service.icon_image:
                service.icon_image = icon_path
                service.save()
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Created service: {service.title} with icon'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Updated service: {service.title} with icon'))
            else:
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Created service: {service.title} (icon file not found)'))
                elif not service.icon_image:
                    self.stdout.write(self.style.WARNING(f'[WARN] Icon file not found for: {service.title} at {full_path}'))

        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Created {created_count} services, Updated {updated_count} services with icons!'))

        # Create Tools
        tools_data = [
            {
                'title': 'Google Search Console',
                'icon': 'insights',
                'description': 'Monitor search performance, identify issues, and optimize visibility in Google search results.',
                'order': 1,
                'icon_file': 'google_search_console.svg',
            },
            {
                'title': 'Ahrefs',
                'icon': 'bar_chart',
                'description': 'Comprehensive backlink analysis, keyword research, and competitor intelligence platform.',
                'order': 2,
                'icon_file': 'ahrefs.svg',
            },
            {
                'title': 'SEMrush',
                'icon': 'speed',
                'description': 'All-in-one SEO toolkit for keyword research, site audit, and competitive analysis.',
                'order': 3,
                'icon_file': 'semrush.svg',
            },
            {
                'title': 'Screaming Frog',
                'icon': 'bug_report',
                'description': 'Website crawler for technical SEO audits, identifying broken links and optimization opportunities.',
                'order': 4,
                'icon_file': 'screaming_frog.svg',
            },
        ]

        tools_created = 0
        tools_updated = 0
        for tool_data in tools_data:
            icon_file = tool_data.pop('icon_file')
            tool, created = SEOAuditTool.objects.get_or_create(
                title=tool_data['title'],
                defaults={
                    **tool_data,
                    'is_active': True,
                }
            )
            
            # Try to assign icon image if file exists
            icon_path = f'services/seo_audit/tool_icons/{icon_file}'
            full_path = os.path.join(settings.MEDIA_ROOT, icon_path)
            
            if os.path.exists(full_path) and not tool.icon_image:
                tool.icon_image = icon_path
                tool.save()
                if created:
                    tools_created += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Created tool: {tool.title} with icon'))
                else:
                    tools_updated += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Updated tool: {tool.title} with icon'))
            else:
                if created:
                    tools_created += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Created tool: {tool.title} (icon file not found)'))
                elif not tool.icon_image:
                    self.stdout.write(self.style.WARNING(f'[WARN] Icon file not found for: {tool.title} at {full_path}'))

        # Create Tool Logos
        logos_data = [
            {'name': 'Google', 'logo_file': 'gsc.svg', 'order': 1},
            {'name': 'Ahrefs', 'logo_file': 'ahrefs.svg', 'order': 2},
            {'name': 'SEMrush', 'logo_file': 'semrush.svg', 'order': 3},
            {'name': 'Moz', 'logo_file': 'moz_pro.svg', 'order': 4},
            {'name': 'Screaming Frog', 'logo_file': 'screaming_frog.svg', 'order': 5},
            {'name': 'Lighthouse', 'logo_file': 'ga4.svg', 'order': 6},  # Using GA4 as placeholder for Lighthouse
        ]

        logos_created = 0
        logos_updated = 0
        for logo_data in logos_data:
            logo_file = logo_data.pop('logo_file')
            logo, created = SEOAuditToolLogo.objects.get_or_create(
                name=logo_data['name'],
                defaults={
                    **logo_data,
                    'is_active': True,
                }
            )
            
            # Try to assign logo file if exists
            logo_path = f'services/seo_audit/tool_logos/{logo_file}'
            full_path = os.path.join(settings.MEDIA_ROOT, logo_path)
            
            if os.path.exists(full_path) and not logo.logo:
                logo.logo = logo_path
                logo.save()
                if created:
                    logos_created += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Created logo: {logo.name} with image'))
                else:
                    logos_updated += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Updated logo: {logo.name} with image'))
            else:
                if created:
                    logos_created += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Created logo: {logo.name} (logo file not found)'))
                elif not logo.logo:
                    self.stdout.write(self.style.WARNING(f'[WARN] Logo file not found for: {logo.name} at {full_path}'))

        # Create Benefits
        benefits_data = [
            {
                'title': 'Increased Organic Traffic',
                'icon': 'trending_up',
                'description': '475% average traffic increase within 6 months',
                'order': 1,
                'icon_file': 'increased_organic_traffic.svg',
            },
            {
                'title': 'Better Search Rankings',
                'icon': 'visibility',
                'description': 'Rank higher for target keywords and phrases',
                'order': 2,
                'icon_file': 'better_search_rankings.svg',
            },
            {
                'title': 'Higher Conversion Rates',
                'icon': 'monetization_on',
                'description': 'Qualified traffic that converts into customers',
                'order': 3,
                'icon_file': 'higher_conversion_rates.svg',
            },
            {
                'title': 'Improved Site Performance',
                'icon': 'speed',
                'description': 'Faster load times and better user experience',
                'order': 4,
                'icon_file': 'improved_site_performance.svg',
            },
        ]

        benefits_created = 0
        benefits_updated = 0
        for benefit_data in benefits_data:
            icon_file = benefit_data.pop('icon_file')
            benefit, created = SEOAuditBenefit.objects.get_or_create(
                title=benefit_data['title'],
                defaults={
                    **benefit_data,
                    'is_active': True,
                }
            )
            
            # Try to assign icon image if file exists
            icon_path = f'services/seo_audit/benefit_icons/{icon_file}'
            full_path = os.path.join(settings.MEDIA_ROOT, icon_path)
            
            if os.path.exists(full_path) and not benefit.icon_image:
                benefit.icon_image = icon_path
                benefit.save()
                if created:
                    benefits_created += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Created benefit: {benefit.title} with icon'))
                else:
                    benefits_updated += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Updated benefit: {benefit.title} with icon'))
            else:
                if created:
                    benefits_created += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Created benefit: {benefit.title} (icon file not found)'))
                elif not benefit.icon_image:
                    self.stdout.write(self.style.WARNING(f'[WARN] Icon file not found for: {benefit.title} at {full_path}'))

        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Created {tools_created} tools, {logos_created} logos, Updated {logos_updated} logos!'))
        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Created {benefits_created} benefits, Updated {benefits_updated} benefits with icons!'))
        self.stdout.write(self.style.SUCCESS('SEO Audit page initial data populated successfully!'))

