"""
Management command to populate AI Solutions page with initial data
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from website.models import (
    AISolutionsHero, AIService, AITechnology, AITechnologyDetail,
    AIImplementationStep, AIROIMetric, AIPerformanceMetric, 
    AITestimonial, AISolutionsCTA
)
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Populate AI Solutions page with initial data and download technology logos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting AI Solutions page population...'))
        
        # Create Hero Section
        self.create_hero_section()
        
        # Create AI Services
        self.create_ai_services()
        
        # Create AI Technologies with logos
        self.create_ai_technologies()
        
        # Create AI Technology Details
        self.create_technology_details()
        
        # Create Implementation Steps
        self.create_implementation_steps()
        
        # Create ROI Metrics
        self.create_roi_metrics()
        
        # Create Performance Metrics
        self.create_performance_metrics()
        
        # Create Testimonials
        self.create_testimonials()
        
        # Create CTA Section
        self.create_cta_section()
        
        self.stdout.write(self.style.SUCCESS('✅ AI Solutions page populated successfully!'))

    def download_image(self, url, filename):
        """Download image from URL"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return ContentFile(response.content, name=filename)
            else:
                self.stdout.write(self.style.WARNING(f'Failed to download {filename}: Status {response.status_code}'))
                return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Error downloading {filename}: {str(e)}'))
            return None

    def create_hero_section(self):
        """Create or update hero section"""
        hero, created = AISolutionsHero.objects.update_or_create(
            id=1,
            defaults={
                'badge_icon': 'psychology',
                'badge_text': 'Next-Gen AI Technology',
                'headline': 'Transform Your Business with <span class="text-primary">AI-Powered</span> Intelligence',
                'description': 'From intelligent chatbots to predictive analytics and machine learning models. We build custom AI solutions that automate workflows, enhance decision-making, and drive exponential growth.',
                'cta_primary_text': 'Start AI Transformation',
                'cta_primary_url': '/contact',
                'cta_secondary_text': 'View AI Case Studies',
                'cta_secondary_url': '/case-studies',
                'metric_title': 'AI Impact Forecast',
                'metric_main': '85% Cost Reduction',
                'automation_rate': 94,
                'time_saved': '2,400h/mo',
                'is_active': True,
            }
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Hero section {"created" if created else "updated"}'))

    def create_ai_services(self):
        """Create AI services"""
        services = [
            {
                'icon': 'smart_toy',
                'title': 'AI Chatbots & Agents',
                'description': 'Intelligent conversational AI that handles customer queries 24/7 with human-like understanding.',
                'feature_1': 'Natural Language Processing',
                'feature_2': 'Multi-Platform Integration',
                'order': 1,
            },
            {
                'icon': 'model_training',
                'title': 'Machine Learning Models',
                'description': 'Custom ML algorithms that predict trends, automate decisions, and optimize operations.',
                'feature_1': 'Predictive Analytics',
                'feature_2': 'Pattern Recognition',
                'order': 2,
            },
            {
                'icon': 'visibility',
                'title': 'Computer Vision',
                'description': 'Image and video analysis for object detection, facial recognition, and quality control.',
                'feature_1': 'Object Detection',
                'feature_2': 'OCR & Document Processing',
                'order': 3,
            },
            {
                'icon': 'precision_manufacturing',
                'title': 'Process Automation',
                'description': 'RPA and AI-driven workflow automation that eliminates repetitive tasks and human error.',
                'feature_1': 'Workflow Optimization',
                'feature_2': 'Data Entry Automation',
                'order': 4,
            },
        ]
        
        for service_data in services:
            service, created = AIService.objects.update_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Service: {service.title}'))

    def create_ai_technologies(self):
        """Create AI technologies with logos"""
        # SVG logos from reliable CDNs
        technologies = [
            {
                'name': 'OpenAI',
                'description': 'Advanced language models for content generation, analysis, and conversation',
                'logo_url': 'https://static.vecteezy.com/system/resources/previews/022/227/364/non_2x/openai-chatgpt-logo-icon-free-png.png',
                'order': 1,
            },
            {
                'name': 'TensorFlow',
                'description': 'Deep learning framework for custom neural networks',
                'logo_url': 'https://cdn.simpleicons.org/tensorflow/FF6F00',
                'order': 2,
            },
            {
                'name': 'PyTorch',
                'description': 'Machine learning framework for research and production',
                'logo_url': 'https://cdn.simpleicons.org/pytorch/EE4C2C',
                'order': 3,
            },
            {
                'name': 'LangChain',
                'description': 'Framework for building applications with LLMs',
                'logo_url': 'https://cdn.simpleicons.org/langchain/1C3C3C',
                'order': 4,
            },
            {
                'name': 'Hugging Face',
                'description': 'State-of-the-art NLP models and transformers',
                'logo_url': 'https://cdn.simpleicons.org/huggingface/FFD21E',
                'order': 5,
            },
            {
                'name': 'AWS AI',
                'description': 'Scalable cloud AI and ML services',
                'logo_url': 'https://cdn.worldvectorlogo.com/logos/aws-2.svg',
                'order': 6,
            },
        ]
        
        for tech_data in technologies:
            tech, created = AITechnology.objects.update_or_create(
                name=tech_data['name'],
                defaults={
                    'description': tech_data['description'],
                    'order': tech_data['order'],
                    'is_active': True,
                }
            )
            
            # Download and save logo
            if not tech.logo or created:
                logo_file = self.download_image(tech_data['logo_url'], f"{tech_data['name'].lower().replace(' ', '_')}.svg")
                if logo_file:
                    tech.logo.save(f"{tech_data['name'].lower().replace(' ', '_')}.svg", logo_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f'✓ Technology: {tech.name} (logo downloaded)'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'✓ Technology: {tech.name} (logo failed)'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Technology: {tech.name}'))

    def create_technology_details(self):
        """Create technology detail descriptions"""
        details = [
            {
                'icon': 'psychology',
                'title': 'OpenAI & GPT Models',
                'description': 'Advanced language models for content generation, analysis, and conversation.',
                'order': 1,
            },
            {
                'icon': 'hub',
                'title': 'TensorFlow & PyTorch',
                'description': 'Deep learning frameworks for custom neural networks and complex AI models.',
                'order': 2,
            },
            {
                'icon': 'cloud',
                'title': 'Cloud AI Services',
                'description': 'AWS SageMaker, Google Cloud AI, Azure ML for scalable deployment.',
                'order': 3,
            },
        ]
        
        for detail_data in details:
            detail, created = AITechnologyDetail.objects.update_or_create(
                title=detail_data['title'],
                defaults=detail_data
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Tech Detail: {detail.title}'))

    def create_implementation_steps(self):
        """Create implementation process steps"""
        steps = [
            {
                'step_number': 1,
                'title': 'Use Case Analysis',
                'description': 'Identify high-impact processes and pain points where AI can drive immediate value and efficiency gains.',
                'order': 1,
            },
            {
                'step_number': 2,
                'title': 'Data Preparation',
                'description': 'Collect, clean, and structure your data to ensure optimal model training and accuracy.',
                'order': 2,
            },
            {
                'step_number': 3,
                'title': 'Model Development',
                'description': 'Build, train, and fine-tune custom AI models using the latest algorithms and frameworks.',
                'order': 3,
            },
            {
                'step_number': 4,
                'title': 'Deploy & Optimize',
                'description': 'Seamless integration with continuous monitoring, retraining, and performance optimization.',
                'order': 4,
            },
        ]
        
        for step_data in steps:
            step, created = AIImplementationStep.objects.update_or_create(
                step_number=step_data['step_number'],
                defaults=step_data
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Step {step.step_number}: {step.title}'))

    def create_roi_metrics(self):
        """Create ROI metrics"""
        metrics = [
            {
                'icon': 'trending_up',
                'title': '85% Cost Reduction',
                'description': 'Average operational cost savings within 6 months.',
                'order': 1,
            },
            {
                'icon': 'speed',
                'title': '10x Faster Processing',
                'description': 'Automated workflows complete in seconds, not hours.',
                'order': 2,
            },
            {
                'icon': 'analytics',
                'title': '99.4% Accuracy',
                'description': 'Enterprise-grade precision in predictions and decisions.',
                'order': 3,
            },
            {
                'icon': 'schedule',
                'title': '24/7 Availability',
                'description': 'AI systems that never sleep, ensuring continuous operation.',
                'order': 4,
            },
        ]
        
        for metric_data in metrics:
            metric, created = AIROIMetric.objects.update_or_create(
                title=metric_data['title'],
                defaults=metric_data
            )
            self.stdout.write(self.style.SUCCESS(f'✓ ROI Metric: {metric.title}'))

    def create_performance_metrics(self):
        """Create performance metrics with progress bars"""
        metrics = [
            {
                'metric_name': 'Automation Rate',
                'percentage': 94,
                'color': 'green-400',
                'order': 1,
            },
            {
                'metric_name': 'Accuracy Score',
                'percentage': 99,
                'color': 'green-400',
                'order': 2,
            },
            {
                'metric_name': 'Cost Efficiency',
                'percentage': 85,
                'color': 'green-400',
                'order': 3,
            },
            {
                'metric_name': 'User Satisfaction',
                'percentage': 96,
                'color': 'green-400',
                'order': 4,
            },
        ]
        
        for metric_data in metrics:
            metric, created = AIPerformanceMetric.objects.update_or_create(
                metric_name=metric_data['metric_name'],
                defaults=metric_data
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Performance: {metric.metric_name}'))

    def create_testimonials(self):
        """Create AI testimonials"""
        testimonials = [
            {
                'client_name': 'James Robertson',
                'client_position': 'CEO',
                'client_company': 'TechFlow Systems',
                'testimonial_text': "Techlynx Pro's AI chatbot reduced our support ticket volume by 70% while improving customer satisfaction scores. The ROI was evident within the first month.",
                'order': 1,
            },
            {
                'client_name': 'Dr. Maria Chen',
                'client_position': 'CTO',
                'client_company': 'DataPrime Analytics',
                'testimonial_text': 'Their ML models predicted customer churn with 95% accuracy, allowing us to proactively retain high-value clients. Game-changing insights.',
                'order': 2,
            },
        ]
        
        # Note: Photos would need to be downloaded separately if URLs are provided
        for testimonial_data in testimonials:
            testimonial, created = AITestimonial.objects.update_or_create(
                client_name=testimonial_data['client_name'],
                defaults=testimonial_data
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Testimonial: {testimonial.client_name}'))

    def create_cta_section(self):
        """Create or update CTA section"""
        cta, created = AISolutionsCTA.objects.update_or_create(
            id=1,
            defaults={
                'headline': 'Ready to Harness the Power of AI?',
                'description': 'Join forward-thinking enterprises who are gaining competitive advantage through intelligent automation and AI-driven decision making.',
                'cta_primary_text': 'Start Your AI Journey',
                'cta_primary_url': '/contact',
                'cta_secondary_text': 'Schedule Demo',
                'cta_secondary_url': '/contact',
                'footer_text': 'Free AI readiness assessment included with every consultation.',
                'is_active': True,
            }
        )
        self.stdout.write(self.style.SUCCESS(f'✓ CTA section {"created" if created else "updated"}'))
