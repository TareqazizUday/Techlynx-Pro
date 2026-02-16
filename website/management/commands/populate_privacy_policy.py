from django.core.management.base import BaseCommand
from website.models import PrivacyPolicy, PrivacyPolicySection, PrivacyPolicySubsection
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate initial data for Privacy Policy page'

    def handle(self, *args, **kwargs):
        # Create or update Privacy Policy
        policy, created = PrivacyPolicy.objects.get_or_create(
            defaults={
                'title': 'Privacy Policy',
                'last_updated': timezone.now().date(),
                'introduction': 'At Techlynx Pro, we are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website or use our services.',
                'contact_email': 'privacy@techlynxpro.com',
                'contact_url': '/contact/',
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Created Privacy Policy'))
        else:
            self.stdout.write(self.style.WARNING('[INFO] Privacy Policy already exists, updating...'))
            policy.last_updated = timezone.now().date()
            policy.save()

        # Create Sections
        sections_data = [
            {
                'section_number': 1,
                'title': 'Information We Collect',
                'content': 'We collect information that you provide directly to us and information that is automatically collected when you use our services.',
                'order': 1,
                'subsections': [
                    {
                        'title': 'Personal Information',
                        'content': 'We may collect personal information that you voluntarily provide to us when you fill out contact forms, subscribe to our newsletter, register for an account, or communicate with us. This information may include your name, email address, phone number, company name, job title, and any other information you choose to provide.',
                        'order': 1,
                    },
                    {
                        'title': 'Automatically Collected Information',
                        'content': 'When you visit our website, we automatically collect certain information about your device and browsing behavior, including IP address, browser type, operating system, pages visited, time spent on pages, referring website addresses, and device identifiers.',
                        'order': 2,
                    },
                ],
            },
            {
                'section_number': 2,
                'title': 'How We Use Your Information',
                'content': 'We use the information we collect for various purposes, including:',
                'order': 2,
                'subsections': [
                    {
                        'title': 'Service Delivery',
                        'content': 'To provide, maintain, and improve our services',
                        'order': 1,
                    },
                    {
                        'title': 'Communication',
                        'content': 'To respond to your inquiries, send service updates, and provide customer support',
                        'order': 2,
                    },
                    {
                        'title': 'Marketing',
                        'content': 'To send you promotional materials, newsletters, and other marketing communications (with your consent)',
                        'order': 3,
                    },
                    {
                        'title': 'Analytics',
                        'content': 'To analyze website usage, track trends, and understand user preferences',
                        'order': 4,
                    },
                ],
            },
            {
                'section_number': 3,
                'title': 'Information Sharing and Disclosure',
                'content': 'We do not sell, trade, or rent your personal information to third parties. We may share your information only in the following circumstances:',
                'order': 3,
                'subsections': [
                    {
                        'title': 'Service Providers',
                        'content': 'With trusted third-party service providers who assist us in operating our website and conducting our business',
                        'order': 1,
                    },
                    {
                        'title': 'Legal Requirements',
                        'content': 'When required by law, court order, or government regulation',
                        'order': 2,
                    },
                    {
                        'title': 'Business Transfers',
                        'content': 'In connection with a merger, acquisition, or sale of assets',
                        'order': 3,
                    },
                ],
            },
            {
                'section_number': 4,
                'title': 'Data Security',
                'content': 'We implement appropriate technical and organizational security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. However, no method of transmission over the Internet or electronic storage is 100% secure, and we cannot guarantee absolute security.',
                'order': 4,
                'subsections': [],
            },
            {
                'section_number': 5,
                'title': 'Cookies and Tracking Technologies',
                'content': 'We use cookies and similar tracking technologies to collect and store information about your preferences and browsing behavior. You can control cookie preferences through your browser settings, but disabling cookies may limit your ability to use certain features of our website.',
                'order': 5,
                'subsections': [],
            },
            {
                'section_number': 6,
                'title': 'Your Rights and Choices',
                'content': 'Depending on your location, you may have certain rights regarding your personal information, including:',
                'order': 6,
                'subsections': [
                    {
                        'title': 'Access Rights',
                        'content': 'Request access to your personal information',
                        'order': 1,
                    },
                    {
                        'title': 'Correction Rights',
                        'content': 'Request correction of inaccurate information',
                        'order': 2,
                    },
                    {
                        'title': 'Deletion Rights',
                        'content': 'Request deletion of your personal information',
                        'order': 3,
                    },
                    {
                        'title': 'Opt-Out Rights',
                        'content': 'Unsubscribe from marketing communications',
                        'order': 4,
                    },
                ],
            },
            {
                'section_number': 7,
                'title': 'Children\'s Privacy',
                'content': 'Our services are not intended for individuals under the age of 18. We do not knowingly collect personal information from children. If you believe we have collected information from a child, please contact us immediately.',
                'order': 7,
                'subsections': [],
            },
            {
                'section_number': 8,
                'title': 'International Data Transfers',
                'content': 'Your information may be transferred to and processed in countries other than your country of residence. We ensure that appropriate safeguards are in place to protect your information in accordance with this Privacy Policy.',
                'order': 8,
                'subsections': [],
            },
            {
                'section_number': 9,
                'title': 'Changes to This Privacy Policy',
                'content': 'We may update this Privacy Policy from time to time to reflect changes in our practices or for other operational, legal, or regulatory reasons. We will notify you of any material changes by posting the new Privacy Policy on this page and updating the "Last Updated" date.',
                'order': 9,
                'subsections': [],
            },
        ]

        sections_created = 0
        subsections_created = 0

        for section_data in sections_data:
            subsections = section_data.pop('subsections', [])
            section, section_created = PrivacyPolicySection.objects.get_or_create(
                policy=policy,
                section_number=section_data['section_number'],
                defaults={
                    **section_data,
                    'is_active': True,
                }
            )
            
            if section_created:
                sections_created += 1
                self.stdout.write(self.style.SUCCESS(f'[OK] Created section: {section.title}'))
            
            # Create subsections
            for subsection_data in subsections:
                subsection, subsection_created = PrivacyPolicySubsection.objects.get_or_create(
                    section=section,
                    title=subsection_data['title'],
                    defaults={
                        **subsection_data,
                        'is_active': True,
                    }
                )
                if subsection_created:
                    subsections_created += 1

        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Created {sections_created} sections and {subsections_created} subsections!'))
        self.stdout.write(self.style.SUCCESS('Privacy Policy page data populated successfully!'))

