from django.core.management.base import BaseCommand
from website.models import PrivacyPolicy, TermsOfService, PrivacyPolicySection, TermsOfServiceSection
from django.utils import timezone


class Command(BaseCommand):
    help = 'Update Privacy Policy and Terms of Service with content from sections'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n=== Updating Legal Pages Content ===\n'))
        
        # Update Privacy Policy
        self.update_privacy_policy()
        
        # Update Terms of Service
        self.update_terms_of_service()
        
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Legal pages content updated successfully!'))

    def update_privacy_policy(self):
        """Update Privacy Policy with content"""
        policy = PrivacyPolicy.objects.filter(is_active=True).first()
        
        if not policy:
            self.stdout.write(self.style.WARNING('[WARN] Privacy Policy not found. Creating new one...'))
            policy = PrivacyPolicy.objects.create(
                title='Privacy Policy',
                last_updated=timezone.now().date(),
                introduction='At Techlynx Pro, we are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website or use our services.',
                contact_email='privacy@techlynxpro.com',
                contact_url='/contact/',
                is_active=True
            )
        
        # Get all sections and combine into content
        sections = PrivacyPolicySection.objects.filter(policy=policy, is_active=True).order_by('order', 'section_number')
        
        if sections.exists():
            content_parts = []
            for section in sections:
                section_html = f'<h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white mb-4 mt-8 first:mt-0">{section.section_number}. {section.title}</h2>'
                section_html += f'<div class="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">{section.content}</div>'
                
                # Add subsections if any
                subsections = section.subsections.filter(is_active=True).order_by('order')
                if subsections.exists():
                    for idx, subsection in enumerate(subsections, 1):
                        section_html += f'<h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3 mt-5">{section.section_number}.{idx} {subsection.title}</h3>'
                        section_html += f'<div class="text-slate-600 dark:text-slate-400 mb-5 leading-relaxed">{subsection.content}</div>'
                
                content_parts.append(f'<div class="mb-8">{section_html}</div>')
            
            policy.content = '\n'.join(content_parts)
            policy.save()
            self.stdout.write(self.style.SUCCESS('[OK] Privacy Policy content updated from sections'))
        else:
            # Set default content if no sections
            default_content = """
            <div class="mb-12">
                <h2 class="text-3xl font-black text-slate-900 dark:text-white mb-6">1. Information We Collect</h2>
                <div class="text-slate-600 dark:text-slate-400 mb-4 leading-relaxed">
                    <p>We may collect personal information that you voluntarily provide to us when you:</p>
                    <ul class="list-disc list-inside ml-4 space-y-2">
                        <li>Fill out contact forms or request information about our services</li>
                        <li>Subscribe to our newsletter or marketing communications</li>
                        <li>Register for an account or use our services</li>
                        <li>Participate in surveys, contests, or promotions</li>
                        <li>Communicate with us via email, phone, or other channels</li>
                    </ul>
                </div>
            </div>
            <div class="mb-12">
                <h2 class="text-3xl font-black text-slate-900 dark:text-white mb-6">2. How We Use Your Information</h2>
                <div class="text-slate-600 dark:text-slate-400 mb-4 leading-relaxed">
                    <p>We use the information we collect for various purposes, including:</p>
                    <ul class="list-disc list-inside ml-4 space-y-2">
                        <li><strong>Service Delivery:</strong> To provide, maintain, and improve our services</li>
                        <li><strong>Communication:</strong> To respond to your inquiries, send service updates, and provide customer support</li>
                        <li><strong>Marketing:</strong> To send you promotional materials, newsletters, and other marketing communications (with your consent)</li>
                        <li><strong>Analytics:</strong> To analyze website usage, track trends, and understand user preferences</li>
                        <li><strong>Legal Compliance:</strong> To comply with legal obligations and protect our rights</li>
                    </ul>
                </div>
            </div>
            """
            policy.content = default_content
            policy.save()
            self.stdout.write(self.style.SUCCESS('[OK] Privacy Policy content set to default'))

    def update_terms_of_service(self):
        """Update Terms of Service with content"""
        terms = TermsOfService.objects.filter(is_active=True).first()
        
        if not terms:
            self.stdout.write(self.style.WARNING('[WARN] Terms of Service not found. Creating new one...'))
            terms = TermsOfService.objects.create(
                title='Terms of Service',
                last_updated=timezone.now().date(),
                introduction='Please read these Terms of Service carefully before using our website and services. By accessing or using our services, you agree to be bound by these Terms.',
                contact_email='legal@techlynxpro.com',
                contact_url='/contact/',
                is_active=True
            )
        
        # Get all sections and combine into content
        sections = TermsOfServiceSection.objects.filter(terms=terms, is_active=True).order_by('order', 'section_number')
        
        if sections.exists():
            content_parts = []
            for section in sections:
                section_html = f'<h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white mb-4 mt-8 first:mt-0">{section.section_number}. {section.title}</h2>'
                section_html += f'<div class="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">{section.content}</div>'
                
                # Add subsections if any
                subsections = section.subsections.filter(is_active=True).order_by('order')
                if subsections.exists():
                    for idx, subsection in enumerate(subsections, 1):
                        section_html += f'<h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3 mt-5">{section.section_number}.{idx} {subsection.title}</h3>'
                        section_html += f'<div class="text-slate-600 dark:text-slate-400 mb-5 leading-relaxed">{subsection.content}</div>'
                
                content_parts.append(f'<div class="mb-8">{section_html}</div>')
            
            terms.content = '\n'.join(content_parts)
            terms.save()
            self.stdout.write(self.style.SUCCESS('[OK] Terms of Service content updated from sections'))
        else:
            # Set default content if no sections
            default_content = """
            <div class="mb-12">
                <h2 class="text-3xl font-black text-slate-900 dark:text-white mb-6">1. Acceptance of Terms</h2>
                <div class="text-slate-600 dark:text-slate-400 mb-4 leading-relaxed">
                    <p>By accessing and using Techlynx Pro's website and services, you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.</p>
                </div>
            </div>
            <div class="mb-12">
                <h2 class="text-3xl font-black text-slate-900 dark:text-white mb-6">2. Use License</h2>
                <div class="text-slate-600 dark:text-slate-400 mb-4 leading-relaxed">
                    <p>Permission is granted to temporarily access the materials on Techlynx Pro's website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:</p>
                    <ul class="list-disc list-inside ml-4 space-y-2">
                        <li>Modify or copy the materials</li>
                        <li>Use the materials for any commercial purpose or for any public display</li>
                        <li>Attempt to reverse engineer any software contained on the website</li>
                        <li>Remove any copyright or other proprietary notations from the materials</li>
                        <li>Transfer the materials to another person or "mirror" the materials on any other server</li>
                    </ul>
                </div>
            </div>
            """
            terms.content = default_content
            terms.save()
            self.stdout.write(self.style.SUCCESS('[OK] Terms of Service content set to default'))

