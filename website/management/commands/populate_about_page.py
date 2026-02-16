from django.core.management.base import BaseCommand
from website.models import (
    AboutPageSEO, AboutPageHero, AboutPageMissionVision, AboutPageAdvantage,
    AboutPageAdvantageSection, AboutPageTimeline, AboutPageTimelineSection,
    AboutPageTeamMember, AboutPageTeamSection, AboutPageCTA
)


class Command(BaseCommand):
    help = 'Populate About page with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating About page...\n')
        
        # 1. SEO Settings
        seo, created = AboutPageSEO.objects.get_or_create(
            defaults={
                'page_title': 'About Techlynx Pro | US-Based IT Experts with 10+ Years Experience',
                'meta_description': "Meet the team behind 500+ successful IT projects. US-based experts with 10+ years experience in web development, AI solutions, and digital marketing. Our mission: deliver enterprise-grade technology with 98% client retention and 200% average ROI.",
                'meta_keywords': 'about us, IT company, US-based developers, expert team, company mission, technology experts, software development company, digital agency, enterprise solutions, certified professionals',
                'og_title': 'About Techlynx Pro | Expert US-Based IT Team Since 2015',
                'og_description': "10+ years delivering enterprise IT solutions. 500+ projects, 98% retention, 200% ROI. Meet our certified US-based team."
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Created SEO settings'))
        else:
            self.stdout.write(self.style.WARNING('  [!] SEO settings already exist'))
        
        # 2. Hero Section
        hero, created = AboutPageHero.objects.get_or_create(
            defaults={
                'headline': 'Empowering Brands through US-Led Digital Innovation',
                'headline_highlight': 'US-Led',
                'description': "Techlynx Pro delivers high-performance, SEO-first digital marketing and IT solutions with a focus on brand authority and scalable infrastructure.",
                'background_image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCk852bNJ4TF9DLKqBa2lcmZMT8hILNqu0iXjyRBUiyCgkB2wX1pGsLcWPlyubqZY9Bww2JbfOjvcHqj9YwAr1vQFBaJ84mCSeOImFdrOzZANqkByK2K4ArDoErBoKAPpqeIGP7gPEcq4HubNdk771eG4hCuUFPkOfiCq2vGKUJWiOAz6z5hKv-ASOo3eLlCpw8Tmd8flR1-8EFxIer5d4SZVHv3amBI7VZzWJY5L5f5qSU6rH0mb5FlHuRsVLMLME5ptOo--uuft2L',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Created Hero section'))
        else:
            self.stdout.write(self.style.WARNING('  [!] Hero section already exists'))
        
        # 3. Mission & Vision
        mission_vision, created = AboutPageMissionVision.objects.get_or_create(
            defaults={
                'mission_title': 'Our Mission',
                'mission_text': 'To empower businesses with SEO-first strategies and scalable digital infrastructure that drives measurable growth and sustainable market dominance in an ever-evolving digital landscape.',
                'mission_icon': 'target',
                'vision_title': 'Our Vision',
                'vision_text': 'To be the global leader in high-performance IT solutions, setting the universal standard for digital excellence, operational integrity, and client-centric innovation.',
                'vision_icon': 'visibility',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Created Mission & Vision'))
        else:
            self.stdout.write(self.style.WARNING('  [!] Mission & Vision already exists'))
        
        # 4. Advantage Section Header
        advantage_section, created = AboutPageAdvantageSection.objects.get_or_create(
            defaults={
                'badge_text': 'Why Work With Us',
                'title': 'The Techlynx Advantage',
                'description': 'We combine domestic management with global technical excellence to provide a seamless experience for enterprise clients.',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Created Advantage Section'))
        else:
            self.stdout.write(self.style.WARNING('  [!] Advantage Section already exists'))
        
        # 5. Advantages
        advantages_data = [
            {
                'title': '100% US-Based Management',
                'description': 'Direct access to project managers and leadership based in the United States, ensuring clear communication and cultural alignment.',
                'icon': 'public',
                'order': 1
            },
            {
                'title': 'Enterprise Security',
                'description': 'Military-grade data protection and compliance frameworks integrated into every line of code and marketing campaign we execute.',
                'icon': 'security',
                'order': 2
            },
            {
                'title': 'SEO-First Architecture',
                'description': "We don't just build websites; we build visibility. Every technical decision is weighed against its impact on organic search performance.",
                'icon': 'monitoring',
                'order': 3
            }
        ]
        
        for data in advantages_data:
            advantage, created = AboutPageAdvantage.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'icon': data['icon'],
                    'order': data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  [OK] Created Advantage: {data['title']}"))
            else:
                self.stdout.write(self.style.WARNING(f"  [!] Advantage already exists: {data['title']}"))
        
        # 6. Timeline Section Header
        timeline_section, created = AboutPageTimelineSection.objects.get_or_create(
            defaults={
                'title': 'Our Growth Story',
                'description': 'A journey of innovation and excellence since our inception.',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Created Timeline Section'))
        else:
            self.stdout.write(self.style.WARNING('  [!] Timeline Section already exists'))
        
        # 7. Timeline Items
        timeline_data = [
            {
                'year': '2018',
                'title': 'Founding of Techlynx',
                'description': 'Started in Austin, TX with a focus on core SEO services.',
                'position': 'left',
                'order': 1
            },
            {
                'year': '2020',
                'title': 'IT Infrastructure Launch',
                'description': 'Expanded into full-stack IT consulting and cloud infrastructure.',
                'position': 'right',
                'order': 2
            },
            {
                'year': '2022',
                'title': 'Global Expansion',
                'description': 'Opened our first international support hub while maintaining US HQ.',
                'position': 'left',
                'order': 3
            },
            {
                'year': 'Present',
                'title': 'Leading the SEO-First Charge',
                'description': 'Serving 500+ clients across 12 countries with 98% retention.',
                'position': 'right',
                'order': 4
            }
        ]
        
        for data in timeline_data:
            timeline, created = AboutPageTimeline.objects.get_or_create(
                year=data['year'],
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'position': data['position'],
                    'order': data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  [OK] Created Timeline: {data['year']} - {data['title']}"))
            else:
                self.stdout.write(self.style.WARNING(f"  [!] Timeline already exists: {data['year']} - {data['title']}"))
        
        # 8. Team Section Header
        team_section, created = AboutPageTeamSection.objects.get_or_create(
            defaults={
                'title': 'Meet the Leadership',
                'description': 'Decades of combined experience in digital transformation.',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Created Team Section'))
        else:
            self.stdout.write(self.style.WARNING('  [!] Team Section already exists'))
        
        # 9. Team Members
        team_data = [
            {
                'name': 'Michael Sterling',
                'position': 'Founder & CEO',
                'photo_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCmCcdBWQirAfbuiuCJX5UUxlH67NtcMJTEZim0NGW0Yld-rc8wMNghaH4SwhtJe0zdNs9M7Pp4lN22RsIo1PYhLCqlL99GqV5IMNaZ9bxdZCje-t-0iaVZlPaTbHDL4jTNPMb1CQdxLUyR7KVCM0mHW08kWRsXA0mEU4Hs3_Vnubmi-8TABGw_rnMUVTzPzfRnq311d8xMjvAV0CKJpVBWMJLzi3yyBoTlhbsTgsAnnS8jKm9qd6ONNxb-SfK1vx4gxNJLFBDjOBCZ',
                'order': 1
            },
            {
                'name': 'Sarah Jenkins',
                'position': 'Chief Technology Officer',
                'photo_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuDiHnB3GHAfBIK_h7QmZFqp2JDF6V1EhGam0EfT_qIaLjmIpHjH6mbAUtCa6HK1mLqtAmdJ0zCp3wenW6XQAo339LAAdsotqilzgEMC9tJeoN7iSK63QAW-6KQ8QAPKUEVN28imiaAW8UtPYy8WT_funCok_usMx_wQYocK1au3PlsrnB_k2R4-Y_BZIsIR_GS-Jqv-C0PGS3077NqJ9-WM6FqSU1RE5MV-HGwNr2Vg0iKnaZFOm1hFCoEmoZt36EQWXv3hgJE-H-gs',
                'order': 2
            },
            {
                'name': 'David Chen',
                'position': 'Director of SEO Strategy',
                'photo_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCRTYyg27-hDcIsH68FKJ191MybM2Kc-1nuwZTs2wlLtY74cmv5D1ybUtw8quxYUzNGdlJS11yIBfYY7NnAqkwJaNEpAmDvxieZV-97kFwXObGgwxz359JGjZ1Oubn7Y4YDv2v0akoRdY43ecTdfAhqTfPW3ZcRxQvtDBy_Nh6tNRCWRGzpZHfw8JvMd0LXVg1GIa4wk7JGOhNBvXPxM200L2h7zuFdW8ityxaciQ7313Dp2ty8KN7bv68q0zEPPMeu09JeGyZek-ZZ',
                'order': 3
            },
            {
                'name': 'Elena Rodriguez',
                'position': 'Head of Operations',
                'photo_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAShDhKL5bM8crDzfqsqK0QCghIfNDHoao2iVEMRlRcpwWffqWdnHrEhX9pt7BTMgNA_hjPWL8Wt40hx_3rQG2LSIuNntlXtCi9Xy1Fuw7CTGwlbAEehp0-HejkrPrmXEZWuXdkKJ4apGRVKoyW1IEjJ6ZXBLUvCGuR0XHYMRnEJaHy1JWmua-7xQCeMJK7jhwszaiJtnKoqh97BvVB7EzB4wPF9ibfN3AKZ2uQ3fgzCbom901v9IYx1fJr4H6tsmVAxjp0nqkmuXqH',
                'order': 4
            }
        ]
        
        for data in team_data:
            team_member, created = AboutPageTeamMember.objects.get_or_create(
                name=data['name'],
                defaults={
                    'position': data['position'],
                    'photo_url': data['photo_url'],
                    'order': data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  [OK] Created Team Member: {data['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"  [!] Team Member already exists: {data['name']}"))
        
        # 10. CTA Section
        cta, created = AboutPageCTA.objects.get_or_create(
            defaults={
                'headline': 'Ready to elevate your digital presence?',
                'description': "Join the hundreds of businesses scaling faster with Techlynx Pro's SEO-first methodology and US-based expertise.",
                'cta_primary_text': 'Start Your Project',
                'cta_primary_url': '/contact/',
                'cta_secondary_text': 'View Our Work',
                'cta_secondary_url': '/case-studies/',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Created CTA Section'))
        else:
            self.stdout.write(self.style.WARNING('  [!] CTA Section already exists'))
        
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] About page data populated successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now manage all content from the admin panel!'))

