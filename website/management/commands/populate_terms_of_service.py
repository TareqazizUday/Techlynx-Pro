from django.core.management.base import BaseCommand
from website.models import TermsOfService, TermsOfServiceSection, TermsOfServiceSubsection
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate initial data for Terms of Service page'

    def handle(self, *args, **kwargs):
        # Create or update Terms of Service
        terms, created = TermsOfService.objects.get_or_create(
            defaults={
                'title': 'Terms of Service',
                'last_updated': timezone.now().date(),
                'introduction': 'Please read these Terms of Service carefully before using our website and services. By accessing or using our services, you agree to be bound by these Terms.',
                'contact_email': 'legal@techlynxpro.com',
                'contact_url': '/contact/',
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Created Terms of Service'))
        else:
            self.stdout.write(self.style.WARNING('[INFO] Terms of Service already exists, updating...'))
            terms.last_updated = timezone.now().date()
            terms.save()

        # Create Sections
        sections_data = [
            {
                'section_number': 1,
                'title': 'Acceptance of Terms',
                'content': 'By accessing and using Techlynx Pro\'s website and services, you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.',
                'order': 1,
                'subsections': [],
            },
            {
                'section_number': 2,
                'title': 'Use License',
                'content': 'Permission is granted to temporarily access the materials on Techlynx Pro\'s website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:',
                'order': 2,
                'subsections': [
                    {
                        'title': 'Restrictions',
                        'content': 'Modify or copy the materials; use the materials for any commercial purpose or for any public display; attempt to reverse engineer any software contained on the website; remove any copyright or other proprietary notations from the materials; transfer the materials to another person or "mirror" the materials on any other server.',
                        'order': 1,
                    },
                ],
            },
            {
                'section_number': 3,
                'title': 'Service Terms',
                'content': 'When you engage our services, you agree to:',
                'order': 3,
                'subsections': [
                    {
                        'title': 'User Obligations',
                        'content': 'Provide accurate and complete information; maintain the security of your account credentials; use our services in compliance with all applicable laws; not use our services for any illegal or unauthorized purpose; respect intellectual property rights.',
                        'order': 1,
                    },
                ],
            },
            {
                'section_number': 4,
                'title': 'Payment Terms',
                'content': 'Payment terms will be specified in individual service agreements. All fees are due as specified in your service contract. Late payments may result in service suspension or termination.',
                'order': 4,
                'subsections': [],
            },
            {
                'section_number': 5,
                'title': 'Intellectual Property',
                'content': 'All content, features, and functionality of our services are owned by Techlynx Pro and are protected by international copyright, trademark, and other intellectual property laws. You may not reproduce, distribute, or create derivative works without our written permission.',
                'order': 5,
                'subsections': [],
            },
            {
                'section_number': 6,
                'title': 'Limitation of Liability',
                'content': 'In no event shall Techlynx Pro or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on Techlynx Pro\'s website, even if Techlynx Pro or a Techlynx Pro authorized representative has been notified orally or in writing of the possibility of such damage.',
                'order': 6,
                'subsections': [],
            },
            {
                'section_number': 7,
                'title': 'Revisions and Errata',
                'content': 'The materials appearing on Techlynx Pro\'s website could include technical, typographical, or photographic errors. Techlynx Pro does not warrant that any of the materials on its website are accurate, complete, or current. Techlynx Pro may make changes to the materials contained on its website at any time without notice.',
                'order': 7,
                'subsections': [],
            },
            {
                'section_number': 8,
                'title': 'Links to Third-Party Sites',
                'content': 'Our website may contain links to third-party websites. We are not responsible for the content, privacy policies, or practices of any third-party sites. Your use of third-party sites is at your own risk.',
                'order': 8,
                'subsections': [],
            },
            {
                'section_number': 9,
                'title': 'Termination',
                'content': 'We reserve the right to terminate or suspend your access to our services immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms.',
                'order': 9,
                'subsections': [],
            },
            {
                'section_number': 10,
                'title': 'Governing Law',
                'content': 'These Terms shall be governed by and construed in accordance with the laws of the jurisdiction in which Techlynx Pro operates, without regard to its conflict of law provisions.',
                'order': 10,
                'subsections': [],
            },
            {
                'section_number': 11,
                'title': 'Changes to Terms',
                'content': 'We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will provide at least 30 days notice prior to any new terms taking effect.',
                'order': 11,
                'subsections': [],
            },
        ]

        sections_created = 0
        subsections_created = 0

        for section_data in sections_data:
            subsections = section_data.pop('subsections', [])
            section, section_created = TermsOfServiceSection.objects.get_or_create(
                terms=terms,
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
                subsection, subsection_created = TermsOfServiceSubsection.objects.get_or_create(
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
        self.stdout.write(self.style.SUCCESS('Terms of Service page data populated successfully!'))

