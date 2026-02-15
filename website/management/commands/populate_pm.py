from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from website.models import (
    PMHero, PMService, PMTool, PMToolLogo, PMProcess,
    PMBenefit, PMMetric, PMTestimonial, PMCTA
)
import requests
import os

class Command(BaseCommand):
    help = 'Populates Project Management page with data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Starting Project Management Page Data Population ===\n'))
        
        # Clear existing data
        PMHero.objects.all().delete()
        PMService.objects.all().delete()
        PMTool.objects.all().delete()
        PMToolLogo.objects.all().delete()
        PMProcess.objects.all().delete()
        PMBenefit.objects.all().delete()
        PMMetric.objects.all().delete()
        PMTestimonial.objects.all().delete()
        PMCTA.objects.all().delete()
        
        # 1. Hero Section
        self.stdout.write('Creating hero section...')
        hero = PMHero.objects.create(
            badge_icon='task_alt',
            badge_text='#1 Project Management Services',
            headline='<span class="text-primary">On Time, Every Time</span> - Enterprise Project Management',
            description='Transform your project delivery with our proven methodologies. 98.5% project success rate across 500+ completed projects spanning startups to Fortune 500 enterprises.',
            success_rate=98.5,
            ontime_delivery=95,
            under_budget=18,
            client_rating=4.9,
            cta_primary_text='Start Your Project',
            cta_primary_url='/contact/',
            cta_secondary_text='View Case Studies',
            cta_secondary_url='/case-studies/',
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✓ Hero section created'))

        # 2. Services
        self.stdout.write('\nCreating services...')
        services_data = [
            {
                'icon': 'sprint',
                'title': 'Agile & Scrum',
                'description': 'Rapid iteration with 2-week sprints, daily standups, and continuous delivery. Perfect for dynamic requirements and fast-paced environments.',
                'feature_1': 'Certified Scrum Masters',
                'feature_2': 'Sprint velocity tracking',
                'order': 1
            },
            {
                'icon': 'waterfall_chart',
                'title': 'Waterfall & Traditional',
                'description': 'Structured approach with clearly defined phases, comprehensive documentation, and predictable timelines for fixed-scope projects.',
                'feature_1': 'Detailed project plans',
                'feature_2': 'Risk mitigation strategies',
                'order': 2
            },
            {
                'icon': 'hub',
                'title': 'Hybrid Approach',
                'description': 'Best of both worlds - combining Agile flexibility with Waterfall structure. Ideal for complex projects requiring both adaptability and governance.',
                'feature_1': 'Flexible methodology',
                'feature_2': 'Governance compliance',
                'order': 3
            },
            {
                'icon': 'account_tree',
                'title': 'Program Management',
                'description': 'Coordinate multiple interdependent projects, align with strategic objectives, and manage complex stakeholder relationships at scale.',
                'feature_1': 'Multi-project oversight',
                'feature_2': 'Strategic alignment',
                'order': 4
            }
        ]
        
        for service_data in services_data:
            service = PMService.objects.create(**service_data, is_active=True)
            self.stdout.write(f'  ✓ Created: {service.title}')

        # 3. Tools
        self.stdout.write('\nCreating tool features...')
        tools_data = [
            {
                'icon': 'dashboard',
                'title': 'Task Management Platforms',
                'description': 'Comprehensive project tracking with customizable workflows, real-time updates, and team collaboration features. Track every task from inception to completion.',
                'order': 1
            },
            {
                'icon': 'forum',
                'title': 'Communication & Collaboration',
                'description': 'Seamless team communication with integrated chat, video conferencing, and file sharing. Keep everyone aligned and informed in real-time.',
                'order': 2
            },
            {
                'icon': 'bar_chart',
                'title': 'Reporting & Analytics',
                'description': 'Advanced project analytics with burndown charts, resource utilization reports, and comprehensive dashboards. Data-driven decision making at your fingertips.',
                'order': 3
            }
        ]
        
        for tool_data in tools_data:
            tool = PMTool.objects.create(**tool_data, is_active=True)
            self.stdout.write(f'  ✓ Created: {tool.title}')

        # 4. Tool Logos
        self.stdout.write('\nCreating tool logos...')
        logos_data = [
            ('Jira', 'https://cdn.worldvectorlogo.com/logos/jira-1.svg', 1),
            ('Asana', 'https://cdn.worldvectorlogo.com/logos/asana-logo.svg', 2),
            ('Monday.com', 'https://cdn.worldvectorlogo.com/logos/monday-com.svg', 3),
            ('Trello', 'https://cdn.worldvectorlogo.com/logos/trello.svg', 4),
            ('Slack', 'https://cdn.worldvectorlogo.com/logos/slack-new-logo.svg', 5),
            ('MS Project', 'https://cdn.worldvectorlogo.com/logos/microsoft-project-2013.svg', 6),
        ]
        
        downloaded_count = 0
        failed_count = 0
        
        for name, url, order in logos_data:
            try:
                self.stdout.write(f'  Downloading: {name}...')
                response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                
                if response.status_code == 200:
                    logo = PMToolLogo.objects.create(name=name, order=order, is_active=True)
                    logo.logo.save(f'{name.lower().replace(".", "").replace(" ", "_")}.svg', 
                                  ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Downloaded: {name}'))
                    downloaded_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ Failed to download {name}: HTTP {response.status_code}'))
                    failed_count += 1
                    # Create without logo
                    PMToolLogo.objects.create(name=name, order=order, is_active=True)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ✗ Error downloading {name}: {str(e)}'))
                failed_count += 1
                # Create without logo
                PMToolLogo.objects.create(name=name, order=order, is_active=True)
        
        self.stdout.write(f'\n  Summary: {downloaded_count} logos downloaded, {failed_count} failed')

        # 5. Process Steps
        self.stdout.write('\nCreating process steps...')
        process_data = [
            {
                'step_number': 1,
                'title': 'Project Initiation & Planning',
                'description': 'Define scope, identify stakeholders, create detailed project charter, and establish success criteria with comprehensive risk assessment.'
            },
            {
                'step_number': 2,
                'title': 'Execution & Monitoring',
                'description': 'Deploy resources, track progress daily, manage team velocity, and maintain continuous stakeholder communication throughout delivery.'
            },
            {
                'step_number': 3,
                'title': 'Quality Control & Testing',
                'description': 'Rigorous QA processes, comprehensive testing protocols, issue resolution tracking, and quality gate validation at every milestone.'
            },
            {
                'step_number': 4,
                'title': 'Closure & Handover',
                'description': 'Final deliverables, comprehensive documentation, knowledge transfer sessions, and post-project retrospective analysis.'
            }
        ]
        
        for step_data in process_data:
            step = PMProcess.objects.create(**step_data, is_active=True)
            self.stdout.write(f'  ✓ Created: Step {step.step_number}')

        # 6. Benefits
        self.stdout.write('\nCreating benefits...')
        benefits_data = [
            {
                'icon': 'schedule',
                'title': 'Time Efficiency',
                'description': '95% on-time delivery rate with streamlined processes and predictive analytics.',
                'order': 1
            },
            {
                'icon': 'savings',
                'title': 'Budget Control',
                'description': 'Average 18% under budget through optimal resource allocation and risk management.',
                'order': 2
            },
            {
                'icon': 'groups',
                'title': 'Stakeholder Satisfaction',
                'description': 'Clear communication and regular updates ensure all stakeholders stay informed and engaged.',
                'order': 3
            },
            {
                'icon': 'shield',
                'title': 'Risk Mitigation',
                'description': 'Proactive risk identification and management reduces project failures by 85%.',
                'order': 4
            }
        ]
        
        for benefit_data in benefits_data:
            benefit = PMBenefit.objects.create(**benefit_data, is_active=True)
            self.stdout.write(f'  ✓ Created: {benefit.title}')

        # 7. Metrics
        self.stdout.write('\nCreating performance metrics...')
        metrics_data = [
            {'title': 'On-Time Delivery', 'value': '95%', 'percentage': 95, 'order': 1},
            {'title': 'Within Budget', 'value': '92%', 'percentage': 92, 'order': 2},
            {'title': 'Quality Standards Met', 'value': '98.5%', 'percentage': 98.5, 'order': 3},
            {'title': 'Client Satisfaction', 'value': '4.9/5.0', 'percentage': 98, 'order': 4},
        ]
        
        for metric_data in metrics_data:
            metric = PMMetric.objects.create(**metric_data, is_active=True)
            self.stdout.write(f'  ✓ Created: {metric.title}')

        # 8. Testimonials
        self.stdout.write('\nCreating testimonials...')
        testimonials_data = [
            {
                'client_name': 'Thomas Anderson',
                'client_position': 'VP of Operations',
                'client_company': 'FinanceHub',
                'testimonial_text': 'TechLynx delivered our banking platform migration 3 weeks ahead of schedule. Their project management excellence was evident in every sprint. The hybrid approach they employed balanced our compliance needs with agile development perfectly.',
                'order': 1
            },
            {
                'client_name': 'Patricia Lee',
                'client_position': 'CTO',
                'client_company': 'GlobalTech Solutions',
                'testimonial_text': 'Managing a global software rollout across 12 countries seemed impossible until TechLynx took over. Their program management expertise coordinated multiple teams flawlessly. We launched on time and 15% under budget.',
                'order': 2
            }
        ]
        
        downloaded_photos = 0
        for testimonial_data in testimonials_data:
            try:
                # Download random professional photos
                self.stdout.write(f'  Downloading photo for {testimonial_data["client_name"]}...')
                response = requests.get(
                    'https://randomuser.me/api/',
                    params={'gender': 'male' if 'Thomas' in testimonial_data['client_name'] else 'female'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    photo_url = data['results'][0]['picture']['large']
                    photo_response = requests.get(photo_url, timeout=10)
                    
                    if photo_response.status_code == 200:
                        testimonial = PMTestimonial.objects.create(**testimonial_data, is_active=True)
                        testimonial.client_photo.save(
                            f'{testimonial_data["client_name"].lower().replace(" ", "_")}.jpg',
                            ContentFile(photo_response.content), save=True
                        )
                        self.stdout.write(self.style.SUCCESS(f'  ✓ Created with photo: {testimonial.client_name}'))
                        downloaded_photos += 1
                    else:
                        testimonial = PMTestimonial.objects.create(**testimonial_data, is_active=True)
                        self.stdout.write(self.style.WARNING(f'  ⚠ Created without photo: {testimonial.client_name}'))
                else:
                    testimonial = PMTestimonial.objects.create(**testimonial_data, is_active=True)
                    self.stdout.write(self.style.WARNING(f'  ⚠ Created without photo: {testimonial.client_name}'))
            except Exception as e:
                testimonial = PMTestimonial.objects.create(**testimonial_data, is_active=True)
                self.stdout.write(self.style.WARNING(f'  ✗ Error: {str(e)}'))
        
        self.stdout.write(f'\n  Summary: {downloaded_photos}/2 photos downloaded')

        # 9. CTA Section
        self.stdout.write('\nCreating CTA section...')
        cta = PMCTA.objects.create(
            headline='Ready to Deliver Projects Successfully?',
            description="Partner with TechLynx for proven project management excellence. From agile startups to enterprise transformations, we'll ensure your projects finish on time, within budget, and exceed expectations.",
            cta_primary_text='Get Started Today',
            cta_primary_url='/contact/',
            cta_secondary_text='Schedule Consultation',
            cta_secondary_url='/contact/',
            footer_icon='verified_user',
            footer_text='PMP-certified project managers with 15+ years of experience',
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✓ CTA section created'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Project Management Page Data Population Complete ==='))
        self.stdout.write(f'Hero sections: {PMHero.objects.count()}')
        self.stdout.write(f'Services: {PMService.objects.count()}')
        self.stdout.write(f'Tools: {PMTool.objects.count()}')
        self.stdout.write(f'Tool Logos: {PMToolLogo.objects.count()}')
        self.stdout.write(f'Process Steps: {PMProcess.objects.count()}')
        self.stdout.write(f'Benefits: {PMBenefit.objects.count()}')
        self.stdout.write(f'Metrics: {PMMetric.objects.count()}')
        self.stdout.write(f'Testimonials: {PMTestimonial.objects.count()}')
        self.stdout.write(f'CTA sections: {PMCTA.objects.count()}')
        self.stdout.write(self.style.SUCCESS(f'\nTotal records: {PMHero.objects.count() + PMService.objects.count() + PMTool.objects.count() + PMToolLogo.objects.count() + PMProcess.objects.count() + PMBenefit.objects.count() + PMMetric.objects.count() + PMTestimonial.objects.count() + PMCTA.objects.count()}'))
