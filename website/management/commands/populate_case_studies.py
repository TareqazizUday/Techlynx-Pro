from django.core.management.base import BaseCommand
from website.models import CaseStudy


class Command(BaseCommand):
    help = 'Populate case studies with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating case studies...')
        
        # Clear existing case studies
        CaseStudy.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing case studies'))

        case_studies_data = [
            {
                'title': 'Global Logistics Co.',
                'slug': 'global-logistics-co',
                'category': 'Logistics',
                'description': 'Complete cloud migration and automated dispatch engine development for a fleet of 5,000+ vehicles.',
                'detailed_description': 'A leading logistics company faced challenges managing their vast fleet of 5,000+ vehicles across multiple regions. We implemented a comprehensive cloud-based solution with real-time tracking and automated dispatch capabilities.',
                'client_name': 'Global Logistics International',
                'challenge': 'Managing a fleet of 5,000+ vehicles with outdated systems led to inefficiencies, high operational costs, and poor visibility. Manual dispatching caused delays and increased fuel consumption.',
                'solution': 'We developed a cloud-based fleet management system with AI-powered route optimization, real-time GPS tracking, automated dispatch engine, and predictive maintenance alerts. The system integrated with existing ERP and CRM platforms.',
                'results': 'Achieved 45% reduction in operational costs, 60% faster dispatch times, 30% reduction in fuel consumption, and 99.9% system uptime. The ROI was realized within 8 months of implementation.',
                'image_alt_text': 'Modern logistics center with digital tracking systems dashboard',
                'key_result_label': 'Key Result',
                'key_result_value': '45% Ops Reduction',
                'order': 1,
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'HealthTrack Systems',
                'slug': 'healthtrack-systems',
                'category': 'Healthcare',
                'description': 'Scalable patient portal integration with HIPAA-compliant secure messaging and telehealth features.',
                'detailed_description': 'A healthcare provider network needed a modern patient engagement platform that complied with HIPAA regulations while providing seamless telehealth capabilities.',
                'client_name': 'HealthTrack Medical Network',
                'challenge': 'Legacy patient management systems created barriers to patient engagement. No secure messaging, limited telehealth capabilities, and poor mobile experience resulted in decreased patient satisfaction.',
                'solution': 'Developed a HIPAA-compliant patient portal with secure messaging, video consultations, appointment scheduling, prescription management, and health record access. Built with React Native for mobile-first experience.',
                'results': 'Patient engagement increased by 150%, telehealth adoption grew 300%, appointment no-shows decreased by 40%, and patient satisfaction scores improved from 3.2 to 4.7 out of 5.',
                'image_alt_text': 'Mobile healthcare app interface on a smartphone screen',
                'key_result_label': 'User Engagement',
                'key_result_value': '+150% Growth',
                'order': 2,
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'Financier App',
                'slug': 'financier-app',
                'category': 'FinTech',
                'description': 'Aggressive paid media campaign and funnel optimization for a leading investment management platform.',
                'detailed_description': 'An investment management platform struggled with high customer acquisition costs and low conversion rates. We implemented a data-driven marketing strategy with advanced funnel optimization.',
                'client_name': 'Financier Investment Platform',
                'challenge': 'High CAC of $450 per customer, 2.1% conversion rate, and poor targeting resulted in unsustainable growth. Competitive market required more efficient customer acquisition strategies.',
                'solution': 'Implemented multi-channel marketing strategy with AI-powered targeting, conversion rate optimization through A/B testing, retargeting campaigns, and personalized landing pages. Integrated analytics for real-time optimization.',
                'results': 'Achieved 3.5x ROI on ad spend, reduced CAC to $128, increased conversion rate to 7.8%, and generated $4.2M in new assets under management within 6 months.',
                'image_alt_text': 'Financial data analytics dashboard on a desktop computer',
                'key_result_label': 'Ad Spend',
                'key_result_value': '3.5x ROI',
                'order': 3,
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'Urban Realty',
                'slug': 'urban-realty',
                'category': 'Real Estate',
                'description': 'Comprehensive SEO strategy and content marketing for a multi-city luxury real estate agency.',
                'detailed_description': 'A luxury real estate agency operating in 5 major cities needed to improve their online visibility and generate more qualified leads through organic search.',
                'client_name': 'Urban Realty Group',
                'challenge': 'Poor search rankings, limited online visibility, 80% of traffic from paid ads, and high cost per lead. Competitors dominated local search results for high-value keywords.',
                'solution': 'Executed comprehensive SEO strategy including technical optimization, local SEO for each city, content marketing with property guides and market insights, link building, and Google My Business optimization.',
                'results': 'Organic traffic increased by 200%, keyword rankings improved with 45 first-page rankings, lead cost decreased by 60%, and generated $18M in property sales attributed to organic search.',
                'image_alt_text': 'High-end modern apartment building under a clear blue sky',
                'key_result_label': 'Organic Traffic',
                'key_result_value': '+200% Growth',
                'order': 4,
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'CloudFlow SaaS',
                'slug': 'cloudflow-saas',
                'category': 'SaaS',
                'description': 'Architecting a high-availability infrastructure for a real-time collaborative workspace application.',
                'detailed_description': 'A startup building a collaborative workspace tool needed a scalable infrastructure that could handle real-time collaboration for thousands of concurrent users.',
                'client_name': 'CloudFlow Technologies',
                'challenge': 'Slow deployment cycles (4 hours), frequent downtime, inability to scale during peak usage, and poor real-time synchronization affecting user experience.',
                'solution': 'Designed microservices architecture with Kubernetes, implemented CI/CD pipeline, set up auto-scaling, used Redis for real-time features, and implemented comprehensive monitoring with Datadog.',
                'results': 'Deployment time reduced by 60% to 90 minutes, achieved 99.95% uptime, handled 10x user growth seamlessly, and reduced infrastructure costs by 35% through optimized resource allocation.',
                'image_alt_text': 'Data visualization charts showing upward business trends',
                'key_result_label': 'Deployment Speed',
                'key_result_value': '60% Faster',
                'order': 5,
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'EcoRetail Store',
                'slug': 'ecoretail-store',
                'category': 'E-commerce',
                'description': 'Optimizing checkout flow and implementing AI personalization for an organic lifestyle brand.',
                'detailed_description': 'An e-commerce brand selling organic products struggled with cart abandonment and low repeat purchase rates. We implemented AI-driven personalization and UX optimization.',
                'client_name': 'EcoRetail Organic Store',
                'challenge': 'Cart abandonment rate of 78%, average order value of $45, low repeat purchase rate of 15%, and generic shopping experience not resonating with health-conscious customers.',
                'solution': 'Redesigned checkout flow with one-page checkout, implemented AI product recommendations, personalized email campaigns, loyalty program integration, and mobile optimization.',
                'results': 'Conversion rate increased by 80%, cart abandonment reduced to 42%, average order value increased to $78, repeat purchase rate jumped to 45%, and revenue increased by 150%.',
                'image_alt_text': 'Team of digital marketers collaborating around a large table',
                'key_result_label': 'Conversion Rate',
                'key_result_value': '80% Higher',
                'order': 6,
                'is_active': True,
                'is_featured': True,  # Mark this one as featured for home page
            },
        ]

        created_count = 0
        for data in case_studies_data:
            case_study = CaseStudy.objects.create(**data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {case_study.title}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} case studies!'))
        self.stdout.write(self.style.WARNING('\n📝 Note: Images need to be uploaded through admin panel'))
        self.stdout.write(self.style.WARNING('   or add image URLs to the background_image field'))
