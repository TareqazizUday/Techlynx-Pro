"""
Management command to populate App Development page data
"""

import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from website.models import (
    AppDevHero, AppDevService, AppDevStackFeature, AppDevTechnology,
    AppDevProcess, AppDevFeature, AppDevPerformanceMetric,
    AppDevTestimonial, AppDevCTA
)


class Command(BaseCommand):
    help = 'Populate App Development page with initial data and download SVG icons'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating App Development page...\n')

        # Clear existing data
        AppDevHero.objects.all().delete()
        AppDevService.objects.all().delete()
        AppDevStackFeature.objects.all().delete()
        AppDevTechnology.objects.all().delete()
        AppDevProcess.objects.all().delete()
        AppDevFeature.objects.all().delete()
        AppDevPerformanceMetric.objects.all().delete()
        AppDevTestimonial.objects.all().delete()
        AppDevCTA.objects.all().delete()

        # Create Hero Section
        AppDevHero.objects.create(
            badge_icon='phone_android',
            badge_text='Native & Cross-Platform Apps',
            headline='Build Amazing <span class="text-primary">Mobile Apps</span> That Users Love',
            description='From iOS and Android native apps to cross-platform solutions with React Native and Flutter. We craft intuitive, high-performance mobile experiences that drive engagement and business growth.',
            cta_primary_text='Start Your App Project',
            cta_primary_url='/contact/',
            cta_secondary_text='View App Portfolio',
            cta_secondary_url='/case-studies/',
            engagement_growth=320,
            is_active=True,
            order=1
        )

        # Create Services with SVG icons
        self.stdout.write('Creating services and downloading icons...')
        services = [
            {
                'icon': 'phone_iphone',
                'icon_url': 'https://cdn.svgporn.com/logos/apple.svg',
                'title': 'iOS App Development',
                'description': 'Native Swift and SwiftUI apps optimized for iPhone, iPad, and Apple ecosystem.',
                'feature_1': 'Swift & SwiftUI',
                'feature_2': 'App Store Optimization',
                'order': 1
            },
            {
                'icon': 'android',
                'icon_url': 'https://cdn.svgporn.com/logos/android-icon.svg',
                'title': 'Android App Development',
                'description': 'Modern Kotlin apps that work seamlessly across all Android devices and versions.',
                'feature_1': 'Kotlin & Jetpack Compose',
                'feature_2': 'Google Play Publishing',
                'order': 2
            },
            {
                'icon': 'devices',
                'icon_url': 'https://cdn.svgporn.com/logos/flutter.svg',
                'title': 'Cross-Platform Apps',
                'description': 'Single codebase for iOS and Android using React Native or Flutter frameworks.',
                'feature_1': 'React Native & Flutter',
                'feature_2': 'Cost-Effective Solution',
                'order': 3
            },
            {
                'icon': 'web',
                'icon_url': 'https://cdn.svgporn.com/logos/pwa.svg',
                'title': 'Progressive Web Apps',
                'description': 'App-like experiences that work in browsers with offline capabilities and push notifications.',
                'feature_1': 'Fast & Reliable',
                'feature_2': 'Offline Mode Support',
                'order': 4
            }
        ]

        for service_data in services:
            service = AppDevService.objects.create(
                icon=service_data['icon'],
                title=service_data['title'],
                description=service_data['description'],
                feature_1=service_data['feature_1'],
                feature_2=service_data['feature_2'],
                is_active=True,
                order=service_data['order']
            )

            # Download and save icon
            try:
                response = requests.get(service_data['icon_url'], timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
                    filename = f"{service_data['title'].lower().replace(' ', '_')}.svg"
                    service.icon_image.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {service.title}: Icon added'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ {service.title}: Icon download failed (status {response.status_code})'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ✗ {service.title}: Icon download failed ({str(e)})'))

        # Create Stack Features with SVG icons
        self.stdout.write('\nCreating stack features and downloading icons...')
        stack_features = [
            {
                'icon': 'phone_android',
                'icon_url': 'https://cdn.svgporn.com/logos/swift.svg',
                'title': 'Native iOS & Android',
                'description': 'Swift, SwiftUI, Kotlin, and Jetpack Compose for optimal performance.',
                'order': 1
            },
            {
                'icon': 'sync_alt',
                'icon_url': 'https://cdn.svgporn.com/logos/react.svg',
                'title': 'Cross-Platform Frameworks',
                'description': 'React Native and Flutter for efficient multi-platform development.',
                'order': 2
            },
            {
                'icon': 'cloud_sync',
                'icon_url': 'https://cdn.svgporn.com/logos/firebase.svg',
                'title': 'Backend & Cloud',
                'description': 'Firebase, AWS Amplify, and custom APIs for robust backend infrastructure.',
                'order': 3
            },
            {
                'icon': 'palette',
                'icon_url': 'https://cdn.svgporn.com/logos/figma.svg',
                'title': 'UI/UX Design',
                'description': 'Figma, Adobe XD, and rapid prototyping for stunning user experiences.',
                'order': 4
            }
        ]

        for feature_data in stack_features:
            feature = AppDevStackFeature.objects.create(
                icon=feature_data['icon'],
                title=feature_data['title'],
                description=feature_data['description'],
                is_active=True,
                order=feature_data['order']
            )

            # Download and save icon
            try:
                response = requests.get(feature_data['icon_url'], timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
                    filename = f"{feature_data['title'].lower().replace(' ', '_').replace('&', 'and')}.svg"
                    feature.icon_image.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {feature.title}: Icon added'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ {feature.title}: Icon download failed (status {response.status_code})'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ✗ {feature.title}: Icon download failed ({str(e)})'))

        # Create Technologies with SVG logos
        self.stdout.write('\nCreating technologies and downloading logos...')
        technologies = [
            {'name': 'Swift', 'logo_url': 'https://cdn.svgporn.com/logos/swift.svg', 'order': 1},
            {'name': 'Kotlin', 'logo_url': 'https://cdn.svgporn.com/logos/kotlin.svg', 'order': 2},
            {'name': 'React Native', 'logo_url': 'https://cdn.svgporn.com/logos/react.svg', 'order': 3},
            {'name': 'Flutter', 'logo_url': 'https://cdn.svgporn.com/logos/flutter.svg', 'order': 4},
            {'name': 'Firebase', 'logo_url': 'https://cdn.svgporn.com/logos/firebase.svg', 'order': 5},
            {'name': 'GraphQL', 'logo_url': 'https://cdn.svgporn.com/logos/graphql.svg', 'order': 6}
        ]

        for tech_data in technologies:
            tech = AppDevTechnology.objects.create(
                name=tech_data['name'],
                is_active=True,
                order=tech_data['order']
            )

            # Download and save logo
            try:
                response = requests.get(tech_data['logo_url'], timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
                    filename = f"{tech_data['name'].lower().replace(' ', '_')}.svg"
                    tech.logo.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {tech.name}: Logo added'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ {tech.name}: Logo download failed (status {response.status_code})'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ✗ {tech.name}: Logo download failed ({str(e)})'))

        # Create Process Steps
        AppDevProcess.objects.create(
            step_number=1,
            title='Strategy & Planning',
            description='Define features, user flows, and technical requirements through detailed wireframes and prototypes.',
            is_active=True,
            order=1
        )
        AppDevProcess.objects.create(
            step_number=2,
            title='UI/UX Design',
            description='Create pixel-perfect interfaces with smooth animations and intuitive navigation patterns.',
            is_active=True,
            order=2
        )
        AppDevProcess.objects.create(
            step_number=3,
            title='Development',
            description='Build with agile sprints, continuous testing, and regular demos to ensure alignment.',
            is_active=True,
            order=3
        )
        AppDevProcess.objects.create(
            step_number=4,
            title='Launch & Support',
            description='App Store submission, marketing assets, and ongoing maintenance with feature updates.',
            is_active=True,
            order=4
        )

        # Create Features with SVG icons
        self.stdout.write('\nCreating features and downloading icons...')
        features = [
            {
                'icon': 'security',
                'icon_url': 'https://cdn-icons-png.flaticon.com/512/747/747376.png',
                'title': 'Bank-Level Security',
                'description': 'End-to-end encryption and secure authentication.',
                'order': 1
            },
            {
                'icon': 'notifications',
                'icon_url': 'https://cdn-icons-png.flaticon.com/512/1827/1827368.png',
                'title': 'Push Notifications',
                'description': 'Re-engage users with targeted messaging.',
                'order': 2
            },
            {
                'icon': 'payments',
                'icon_url': 'https://cdn-icons-png.flaticon.com/512/2830/2830284.png',
                'title': 'Payment Integration',
                'description': 'Stripe, PayPal, Apple Pay, Google Pay support.',
                'order': 3
            },
            {
                'icon': 'bar_chart',
                'icon_url': 'https://cdn-icons-png.flaticon.com/512/3242/3242257.png',
                'title': 'Analytics & Tracking',
                'description': 'Deep insights into user behavior and engagement.',
                'order': 4
            }
        ]

        for feature_data in features:
            feature = AppDevFeature.objects.create(
                icon=feature_data['icon'],
                title=feature_data['title'],
                description=feature_data['description'],
                is_active=True,
                order=feature_data['order']
            )

            # Download and save icon (PNG format)
            try:
                response = requests.get(feature_data['icon_url'], timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
                    filename = f"{feature_data['title'].lower().replace(' ', '_').replace('-', '_')}.png"
                    feature.icon_image.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {feature.title}: Icon added'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ {feature.title}: Icon download failed (status {response.status_code})'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ✗ {feature.title}: Icon download failed ({str(e)})'))

        # Create Performance Metrics
        AppDevPerformanceMetric.objects.create(
            title='App Load Time',
            value='<2s',
            percentage=95,
            is_active=True,
            order=1
        )
        AppDevPerformanceMetric.objects.create(
            title='Crash-Free Rate',
            value='99.8%',
            percentage=99,
            is_active=True,
            order=2
        )
        AppDevPerformanceMetric.objects.create(
            title='User Retention (30-day)',
            value='68%',
            percentage=68,
            is_active=True,
            order=3
        )
        AppDevPerformanceMetric.objects.create(
            title='Average Rating',
            value='4.7★',
            percentage=94,
            is_active=True,
            order=4
        )

        # Create Testimonials (photos will be added separately)
        AppDevTestimonial.objects.create(
            client_name='Rachel Kim',
            client_position='Product Manager',
            client_company='FitLife',
            testimonial_text='Our React Native app hit 100K downloads in the first month. The cross-platform approach saved us months of development time and budget.',
            is_active=True,
            order=1
        )
        AppDevTestimonial.objects.create(
            client_name='Michael Torres',
            client_position='Founder',
            client_company='QuickPay',
            testimonial_text='Techlynx Pro built our fintech app with bank-level security. We passed all compliance audits on the first try. Exceptional quality.',
            is_active=True,
            order=2
        )

        # Create CTA Section
        AppDevCTA.objects.create(
            headline='Ready to Build Your Next Mobile App?',
            description='Join successful companies who have launched high-performing mobile apps that users love and that drive real business growth.',
            cta_primary_text='Get Your Free Quote',
            cta_primary_url='/contact/',
            cta_secondary_text='View Pricing Plans',
            cta_secondary_url='/contact/',
            footer_text='Free app strategy session with every project consultation.',
            footer_icon='verified_user',
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('\n✅ App Development page data populated successfully!'))
