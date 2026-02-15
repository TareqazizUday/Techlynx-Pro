from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from website.models import (
    SEOAuditHero, SEOAuditService, SEOAuditTool, SEOAuditToolLogo,
    SEOAuditProcess, SEOAuditResult, SEOAuditBenefit, SEOAuditHealthMetric,
    SEOAuditTestimonial, SEOAuditCTA
)
import requests
import os


class Command(BaseCommand):
    help = 'Populate SEO Audit page with content and download SVG images'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting SEO Audit page population...'))

        # Clear existing data
        SEOAuditHero.objects.all().delete()
        SEOAuditService.objects.all().delete()
        SEOAuditTool.objects.all().delete()
        SEOAuditToolLogo.objects.all().delete()
        SEOAuditProcess.objects.all().delete()
        SEOAuditResult.objects.all().delete()
        SEOAuditBenefit.objects.all().delete()
        SEOAuditHealthMetric.objects.all().delete()
        SEOAuditTestimonial.objects.all().delete()
        SEOAuditCTA.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing data'))

        # Create Hero Section
        hero = SEOAuditHero.objects.create(
            badge_icon='search',
            badge_text='Data-Driven SEO Strategy',
            headline='Dominate Search Rankings with <span class="text-primary">Expert SEO</span> Audits',
            description='Comprehensive technical SEO audits that uncover hidden issues and unlock organic growth. Get actionable insights to outrank competitors and drive qualified traffic that converts.',
            cta_primary_text='Get Free SEO Audit',
            cta_primary_url='/contact/',
            cta_secondary_text='View SEO Results',
            cta_secondary_url='/case-studies/',
            traffic_growth=475,
            domain_authority=68,
            keywords_ranked=1247,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✓ Created Hero section'))

        # Service icons to download
        service_icons = [
            {
                'name': 'technical_seo_audit',
                'url': 'https://cdn.svgporn.com/logos/google-analytics.svg',
                'fallback': 'https://raw.githubusercontent.com/gilbarbara/logos/main/logos/google-analytics.svg'
            },
            {
                'name': 'on-page_seo_analysis',
                'url': 'https://cdn.svgporn.com/logos/google.svg',
                'fallback': 'https://raw.githubusercontent.com/gilbarbara/logos/main/logos/google.svg'
            },
            {
                'name': 'backlink_profile_audit',
                'url': 'https://www.svgrepo.com/download/349330/link.svg',
                'fallback': 'https://www.svgrepo.com/show/522266/link.svg'
            },
            {
                'name': 'competitor_analysis',
                'url': 'https://www.svgrepo.com/download/530659/analytics.svg',
                'fallback': 'https://www.svgrepo.com/show/530659/analytics.svg'
            }
        ]

        # Download service icons
        for icon_data in service_icons:
            try:
                response = requests.get(icon_data['url'], timeout=10)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"✓ Downloaded {icon_data['name']}.svg"))
                else:
                    response = requests.get(icon_data['fallback'], timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(self.style.SUCCESS(f"✓ Downloaded {icon_data['name']}.svg (fallback)"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Failed to download {icon_data['name']}: {str(e)}"))

        # Create SEO Audit Services
        services_data = [
            {
                'icon': 'settings',
                'title': 'Technical SEO Audit',
                'description': 'Crawl analysis, site speed, mobile-friendliness, and Core Web Vitals optimization.',
                'feature_1': 'Site Speed Analysis',
                'feature_2': 'Crawlability Check',
                'order': 1
            },
            {
                'icon': 'description',
                'title': 'On-Page SEO Analysis',
                'description': 'Content quality, keyword optimization, meta tags, and internal linking structure review.',
                'feature_1': 'Content Optimization',
                'feature_2': 'Meta Tag Review',
                'order': 2
            },
            {
                'icon': 'link',
                'title': 'Backlink Profile Audit',
                'description': 'Link quality assessment, toxic link identification, and competitor backlink analysis.',
                'feature_1': 'Link Quality Score',
                'feature_2': 'Toxic Link Detection',
                'order': 3
            },
            {
                'icon': 'leaderboard',
                'title': 'Competitor Analysis',
                'description': 'Identify ranking gaps, competitor keywords, and opportunities to outperform rivals.',
                'feature_1': 'Gap Analysis',
                'feature_2': 'SERP Tracking',
                'order': 4
            }
        ]

        for service_data in services_data:
            SEOAuditService.objects.create(**service_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(services_data)} audit services'))

        # Tool icons to download
        tool_icons = [
            {
                'name': 'advanced_analytics',
                'url': 'https://cdn.svgporn.com/logos/google-analytics.svg',
                'fallback': 'https://raw.githubusercontent.com/gilbarbara/logos/main/logos/google-analytics.svg'
            },
            {
                'name': 'professional_seo_suites',
                'url': 'https://www.svgrepo.com/download/530659/analytics.svg',
                'fallback': 'https://www.svgrepo.com/show/530659/analytics.svg'
            },
            {
                'name': 'performance_testing',
                'url': 'https://www.svgrepo.com/download/530435/time.svg',
                'fallback': 'https://www.svgrepo.com/show/530435/time.svg'
            }
        ]

        # Download tool icons
        for icon_data in tool_icons:
            try:
                response = requests.get(icon_data['url'], timeout=10)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"✓ Downloaded {icon_data['name']}.svg"))
                else:
                    response = requests.get(icon_data['fallback'], timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(self.style.SUCCESS(f"✓ Downloaded {icon_data['name']}.svg (fallback)"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Failed to download {icon_data['name']}: {str(e)}"))

        # Create SEO Tools
        tools_data = [
            {
                'icon': 'analytics',
                'title': 'Advanced Analytics',
                'description': 'Google Analytics 4, Search Console, and custom tracking implementations.',
                'order': 1
            },
            {
                'icon': 'insights',
                'title': 'Professional SEO Suites',
                'description': 'Ahrefs, SEMrush, and Screaming Frog for deep technical analysis.',
                'order': 2
            },
            {
                'icon': 'speed',
                'title': 'Performance Testing',
                'description': 'Lighthouse, PageSpeed Insights, and GTmetrix for speed optimization.',
                'order': 3
            }
        ]

        for tool_data in tools_data:
            SEOAuditTool.objects.create(**tool_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(tools_data)} tool features'))

        # Tool logos to download
        tool_logos_data = [
            {
                'name': 'Ahrefs',
                'url': 'https://cdn.svgporn.com/logos/ahrefs.svg',
                'fallback': 'https://raw.githubusercontent.com/gilbarbara/logos/main/logos/ahrefs.svg',
                'order': 1
            },
            {
                'name': 'SEMrush',
                'url': 'https://cdn.svgporn.com/logos/semrush.svg',
                'fallback': 'https://raw.githubusercontent.com/gilbarbara/logos/main/logos/semrush.svg',
                'order': 2
            },
            {
                'name': 'Moz Pro',
                'url': 'https://cdn.svgporn.com/logos/moz.svg',
                'fallback': 'https://raw.githubusercontent.com/gilbarbara/logos/main/logos/moz.svg',
                'order': 3
            },
            {
                'name': 'Screaming Frog',
                'url': 'https://www.svgrepo.com/download/345700/frog.svg',
                'fallback': 'https://www.svgrepo.com/show/345700/frog.svg',
                'order': 4
            },
            {
                'name': 'GA4',
                'url': 'https://cdn.svgporn.com/logos/google-analytics.svg',
                'fallback': 'https://raw.githubusercontent.com/gilbarbara/logos/main/logos/google-analytics.svg',
                'order': 5
            },
            {
                'name': 'GSC',
                'url': 'https://cdn.svgporn.com/logos/google.svg',
                'fallback': 'https://raw.githubusercontent.com/gilbarbara/logos/main/logos/google.svg',
                'order': 6
            }
        ]

        # Download and create tool logos
        for logo_data in tool_logos_data:
            try:
                response = requests.get(logo_data['url'], timeout=10)
                if response.status_code != 200:
                    response = requests.get(logo_data['fallback'], timeout=10)
                
                if response.status_code == 200:
                    logo = SEOAuditToolLogo.objects.create(
                        name=logo_data['name'],
                        order=logo_data['order'],
                        is_active=True
                    )
                    
                    # Save the image
                    filename = f"{logo_data['name'].lower().replace(' ', '_')}.svg"
                    logo.logo.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f"✓ Downloaded and saved {logo_data['name']} logo"))
                else:
                    self.stdout.write(self.style.ERROR(f"✗ Failed to download {logo_data['name']} logo"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Failed to download {logo_data['name']} logo: {str(e)}"))

        # Create Process Steps
        process_steps = [
            {
                'step_number': 1,
                'title': 'Data Collection',
                'description': 'Comprehensive site crawl, analytics review, and competitive landscape analysis.'
            },
            {
                'step_number': 2,
                'title': 'Issue Identification',
                'description': 'Uncover technical errors, content gaps, and ranking opportunities.'
            },
            {
                'step_number': 3,
                'title': 'Action Plan',
                'description': 'Prioritized recommendations with clear implementation steps and timelines.'
            },
            {
                'step_number': 4,
                'title': 'Implementation',
                'description': 'Execute fixes, track progress, and continuously optimize for better rankings.'
            }
        ]

        for step_data in process_steps:
            SEOAuditProcess.objects.create(**step_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(process_steps)} process steps'))

        # Create Results Section
        results = SEOAuditResult.objects.create(
            headline='Proven SEO Results That Drive Growth',
            description="Our SEO audits don't just identify problems—they unlock massive organic growth opportunities that transform your search visibility and revenue.",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✓ Created Results section'))

        # Benefit icons to download
        benefit_icons = [
            {
                'name': '475%_traffic_growth',
                'url': 'https://www.svgrepo.com/download/530488/trending-up.svg',
                'fallback': 'https://www.svgrepo.com/show/530488/trending-up.svg'
            },
            {
                'name': 'top_3_rankings',
                'url': 'https://www.svgrepo.com/download/530454/trophy.svg',
                'fallback': 'https://www.svgrepo.com/show/530454/trophy.svg'
            },
            {
                'name': 'technical_excellence',
                'url': 'https://www.svgrepo.com/download/530430/settings.svg',
                'fallback': 'https://www.svgrepo.com/show/530430/settings.svg'
            },
            {
                'name': 'brand_visibility',
                'url': 'https://www.svgrepo.com/download/530463/view.svg',
                'fallback': 'https://www.svgrepo.com/show/530463/view.svg'
            }
        ]

        # Download benefit icons
        for icon_data in benefit_icons:
            try:
                response = requests.get(icon_data['url'], timeout=10)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"✓ Downloaded {icon_data['name']}.svg"))
                else:
                    response = requests.get(icon_data['fallback'], timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(self.style.SUCCESS(f"✓ Downloaded {icon_data['name']}.svg (fallback)"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Failed to download {icon_data['name']}: {str(e)}"))

        # Create Benefits
        benefits_data = [
            {
                'icon': 'trending_up',
                'title': '475% Traffic Growth',
                'description': 'Average organic traffic increase within 6 months.',
                'order': 1
            },
            {
                'icon': 'emoji_events',
                'title': 'Top 3 Rankings',
                'description': 'Achieve page 1 positions for high-value keywords.',
                'order': 2
            },
            {
                'icon': 'build',
                'title': 'Technical Excellence',
                'description': 'Fix critical errors affecting crawlability and indexing.',
                'order': 3
            },
            {
                'icon': 'visibility',
                'title': 'Brand Visibility',
                'description': 'Dominate SERPs for your industry\'s key search terms.',
                'order': 4
            }
        ]

        for benefit_data in benefits_data:
            SEOAuditBenefit.objects.create(**benefit_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(benefits_data)} benefits'))

        # Create Health Metrics
        health_metrics = [
            {
                'title': 'Technical SEO',
                'score': 92,
                'percentage': 92,
                'order': 1
            },
            {
                'title': 'Content Quality',
                'score': 88,
                'percentage': 88,
                'order': 2
            },
            {
                'title': 'Backlink Profile',
                'score': 85,
                'percentage': 85,
                'order': 3
            },
            {
                'title': 'User Experience',
                'score': 96,
                'percentage': 96,
                'order': 4
            }
        ]

        for metric_data in health_metrics:
            SEOAuditHealthMetric.objects.create(**metric_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(health_metrics)} health metrics'))

        # Create Testimonials
        testimonials_data = [
            {
                'client_name': 'David Martinez',
                'client_position': 'Marketing Director',
                'client_company': 'EcoStore',
                'testimonial_text': 'The technical SEO audit uncovered 200+ issues we didn\'t know existed. After implementing their fixes, our organic traffic tripled in 4 months.',
                'order': 1
            },
            {
                'client_name': 'Jennifer Liu',
                'client_position': 'CEO',
                'client_company': 'LegalPro',
                'testimonial_text': 'Their competitor analysis revealed untapped keyword opportunities. We\'re now ranking #1 for our most valuable search terms. ROI is incredible.',
                'order': 2
            }
        ]

        for testimonial_data in testimonials_data:
            SEOAuditTestimonial.objects.create(**testimonial_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(testimonials_data)} testimonials'))

        # Create CTA
        cta = SEOAuditCTA.objects.create(
            headline='Ready to Unlock Your SEO Potential?',
            description='Get a comprehensive SEO audit that reveals exactly what\'s holding you back and how to achieve breakthrough organic growth.',
            cta_primary_text='Get Free SEO Analysis',
            cta_primary_url='/contact/',
            cta_secondary_text='View Audit Samples',
            cta_secondary_url='/contact/',
            footer_text='Free 50-point SEO checklist included with every consultation.',
            footer_icon='verified_user',
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✓ Created CTA section'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('SEO Audit Page Population Complete!'))
        self.stdout.write(self.style.SUCCESS(f'Hero: 1'))
        self.stdout.write(self.style.SUCCESS(f'Services: {SEOAuditService.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Tools: {SEOAuditTool.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Tool Logos: {SEOAuditToolLogo.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Process Steps: {SEOAuditProcess.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Results Section: 1'))
        self.stdout.write(self.style.SUCCESS(f'Benefits: {SEOAuditBenefit.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Health Metrics: {SEOAuditHealthMetric.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Testimonials: {SEOAuditTestimonial.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'CTA: 1'))
        self.stdout.write(self.style.SUCCESS('='*50))
