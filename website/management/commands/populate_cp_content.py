from django.core.management.base import BaseCommand
from website.models import CPService, CPTool, CPBenefit, CPProcessStep, CPMetric, CPTestimonial


class Command(BaseCommand):
    help = 'Populate Content Production page with complete data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating Content Production data...")

        # Clear existing data
        CPService.objects.all().delete()
        CPTool.objects.all().delete()
        CPBenefit.objects.all().delete()
        CPProcessStep.objects.all().delete()
        CPMetric.objects.all().delete()
        CPTestimonial.objects.all().delete()

        # Services
        services = [
            {
                'title': 'Blog & Article Writing',
                'icon': 'article',
                'description': 'SEO-optimized blog posts, thought leadership articles, and long-form content that ranks.',
                'features': [
                    'SEO Content Strategy',
                    'Keyword Research',
                    'Content Optimization',
                    'Thought Leadership'
                ],
                'color_scheme': 'blue',
                'order': 1
            },
            {
                'title': 'Video Production',
                'icon': 'videocam',
                'description': 'Explainer videos, product demos, testimonials, and social video content optimized for engagement.',
                'features': [
                    'Scriptwriting',
                    'Video Editing',
                    'Motion Graphics',
                    'Social Video'
                ],
                'color_scheme': 'purple',
                'order': 2
            },
            {
                'title': 'Graphic Design',
                'icon': 'palette',
                'description': 'Eye-catching infographics, social media graphics, banners, and visual assets that stand out.',
                'features': [
                    'Infographics',
                    'Social Graphics',
                    'Brand Assets',
                    'Visual Design'
                ],
                'color_scheme': 'orange',
                'order': 3
            },
            {
                'title': 'Social Media Content',
                'icon': 'campaign',
                'description': 'Platform-specific content calendars, posts, stories, and reels that drive engagement.',
                'features': [
                    'Content Calendars',
                    'Copywriting',
                    'Platform Strategy',
                    'Engagement'
                ],
                'color_scheme': 'green',
                'order': 4
            },
        ]

        for service_data in services:
            CPService.objects.create(**service_data)
            self.stdout.write(f"✓ Created service: {service_data['title']}")

        # Tools
        tools = [
            {
                'name': 'Adobe Creative Cloud',
                'category': 'Design Suite',
                'description': 'Adobe Creative Cloud, Figma, and Canva for stunning visual content.',
                'icon': 'draw',
                'icon_image': 'services/content_production/tool_icons/adobe_cc.svg',
                'order': 1
            },
            {
                'name': 'Figma',
                'category': 'Design Suite',
                'description': 'Collaborative design tool for stunning visual content.',
                'icon': 'design_services',
                'icon_image': 'services/content_production/tool_icons/figma.svg',
                'order': 2
            },
            {
                'name': 'Premiere Pro',
                'category': 'Video Editing',
                'description': 'Adobe Premiere Pro, Final Cut Pro, and DaVinci Resolve for professional videos.',
                'icon': 'movie_edit',
                'icon_image': 'services/content_production/tool_icons/premiere.svg',
                'order': 3
            },
            {
                'name': 'Canva',
                'category': 'Design Suite',
                'description': 'Easy-to-use design platform for quick visual content.',
                'icon': 'image',
                'icon_image': 'services/content_production/tool_icons/canva.svg',
                'order': 4
            },
            {
                'name': 'WordPress',
                'category': 'Content Management',
                'description': 'WordPress, HubSpot, and ContentStack for seamless publishing.',
                'icon': 'edit_note',
                'icon_image': 'services/content_production/tool_icons/wordpress.svg',
                'order': 5
            },
            {
                'name': 'HubSpot',
                'category': 'Content Management',
                'description': 'Marketing platform for content management and distribution.',
                'icon': 'hub',
                'icon_image': 'services/content_production/tool_icons/hubspot.svg',
                'order': 6
            },
        ]

        for tool_data in tools:
            CPTool.objects.create(**tool_data)
            self.stdout.write(f"✓ Created tool: {tool_data['name']}")

        # Benefits/Results
        benefits = [
            {
                'title': '385% Engagement Boost',
                'description': 'Average increase across social and blog content.',
                'icon': 'trending_up',
                'metric_value': '385%',
                'order': 1
            },
            {
                'title': 'Page 1 Rankings',
                'description': '92% of blog posts rank on Google\'s first page.',
                'icon': 'search',
                'metric_value': '92%',
                'order': 2
            },
            {
                'title': '3.2x More Shares',
                'description': 'Content gets shared 3x more than industry average.',
                'icon': 'share',
                'metric_value': '3.2x',
                'order': 3
            },
            {
                'title': 'Higher Conversions',
                'description': 'Content-driven leads convert at 2.8x better rates.',
                'icon': 'conversion_path',
                'metric_value': '2.8x',
                'order': 4
            },
        ]

        for benefit_data in benefits:
            CPBenefit.objects.create(**benefit_data)
            self.stdout.write(f"✓ Created benefit: {benefit_data['title']}")

        # Process Steps
        process_steps = [
            {
                'step_number': 1,
                'title': 'Strategy & Planning',
                'description': 'Audience research, content topics, keyword analysis, and editorial calendar.'
            },
            {
                'step_number': 2,
                'title': 'Content Creation',
                'description': 'Writing, design, video production, and asset creation by expert creators.'
            },
            {
                'step_number': 3,
                'title': 'Review & Optimize',
                'description': 'Quality assurance, SEO optimization, and revisions based on feedback.'
            },
            {
                'step_number': 4,
                'title': 'Publish & Track',
                'description': 'Content distribution, performance monitoring, and continuous improvement.'
            },
        ]

        for step_data in process_steps:
            CPProcessStep.objects.create(**step_data)
            self.stdout.write(f"✓ Created process step: {step_data['title']}")

        # Metrics
        metrics = [
            {
                'name': 'Engagement Rate',
                'value': '8.7%',
                'percentage': 87,
                'color_class': 'green-400',
                'order': 1
            },
            {
                'name': 'SEO Score',
                'value': '94/100',
                'percentage': 94,
                'color_class': 'green-400',
                'order': 2
            },
            {
                'name': 'Content Velocity',
                'value': '45/month',
                'percentage': 90,
                'color_class': 'green-400',
                'order': 3
            },
            {
                'name': 'Client Satisfaction',
                'value': '4.9/5.0',
                'percentage': 98,
                'color_class': 'green-400',
                'order': 4
            },
        ]

        for metric_data in metrics:
            CPMetric.objects.create(**metric_data)
            self.stdout.write(f"✓ Created metric: {metric_data['name']}")

        # Testimonials
        testimonials = [
            {
                'client_name': 'Sarah Thompson',
                'client_position': 'Marketing Director',
                'client_company': 'GreenLife',
                'client_photo': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCSOi_qlLJG0cA7bB7AJTaMW-k_iOXB8SjLZhyp_QwjpXpzWSGZQ81VInZw9-OGALxY51S3iHWNco6afjwiFyrkJ15m9LvprbpkUlSdCx7S0T3EjgRG6Woxry81B2_GWODy6eLJPtjKTbFE5HYk1SnMjDb-7eo1KeBggdqne1jqk1A8SjsD80bWI72x2z9OA6B1bxaB6kNm7vpN7DCm__NfYj7ksaE7mgFJ86PtCWEgVetE7IqtF4CAKHeCgAI3mhnaEO8MBdFBiwzX',
                'testimonial_text': 'Their blog content increased our organic traffic by 320% in 6 months. Every post ranks on page 1. Absolutely phenomenal quality and strategy.',
                'order': 1
            },
            {
                'client_name': 'Marcus Bennett',
                'client_position': 'Brand Manager',
                'client_company': 'TechWave',
                'client_photo': 'https://lh3.googleusercontent.com/aida-public/AB6AXuA8pDDzP6BfevE_JnONcZ529Z_YB1pMIupHHa3rmte_LACgxKO5ewO678gNiI4-5-uoGJ6Aa4DwaAhfsjxvxAeA8WmE27XXqJmgKtMVIdHv4VqwKQmEwklfkjPYYA3E8A6WfeO3LY2l0-OxlSnKvI4xWL5W-DHhb0D3iWsrRi-CsIVm4LwfoZA4ovW1ehUZ5a7r1IWGiU-RBLfJtm3bbvHj7Q9NtrSWDIV-g6PMgMHIsZZv89Doq0oVI_X8YMbZl_lga2YBHQIlAaF3',
                'testimonial_text': 'The video content they produced for our product launch went viral—2.5M views in the first week. Creative, professional, and on-brand.',
                'order': 2
            },
        ]

        for testimonial_data in testimonials:
            CPTestimonial.objects.create(**testimonial_data)
            self.stdout.write(f"✓ Created testimonial: {testimonial_data['client_name']}")

        self.stdout.write(self.style.SUCCESS('\n✅ All Content Production data has been populated successfully!'))
