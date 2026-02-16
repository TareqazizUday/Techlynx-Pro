from django.core.management.base import BaseCommand
from website.models import TestimonialsPageMetric


class Command(BaseCommand):
    help = 'Populate testimonials page metrics section with initial data'

    def handle(self, *args, **kwargs):
        # Clear existing metrics
        TestimonialsPageMetric.objects.all().delete()
        
        metrics = [
            {
                'value': '340%',
                'title': 'Average Traffic Growth',
                'description': 'Organic traffic increase within 6 months',
                'color': 'blue-500',
                'order': 1
            },
            {
                'value': '2,200%',
                'title': 'Revenue Increase',
                'description': 'From $2K to $45K monthly revenue',
                'color': 'green-500',
                'order': 2
            },
            {
                'value': '98%',
                'title': 'Client Satisfaction',
                'description': 'Consistently rated 5-star service',
                'color': 'purple-500',
                'order': 3
            },
            {
                'value': '500+',
                'title': 'Projects Completed',
                'description': 'Successful implementations delivered',
                'color': 'orange-500',
                'order': 4
            }
        ]
        
        created_count = 0
        for metric_data in metrics:
            TestimonialsPageMetric.objects.create(**metric_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'✓ Created metric: {metric_data["value"]} - {metric_data["title"]}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} testimonials page metrics!'))
