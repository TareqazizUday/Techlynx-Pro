import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techlynx_project.settings')
django.setup()

from website.models import BlogPost, Testimonial

def populate_blog_images():
    """Add images to blog posts"""
    print("\n=== Populating Blog Images ===\n")
    
    blog_posts = BlogPost.objects.all()
    
    # Map blog posts to existing images in media/blog/
    blog_image_mapping = {
        "Optimizing Cloud Infrastructure for 2024 Scalability": "services/web-development_8ihFnF4.jpg",
        "The ROI of Omnichannel Marketing in B2B Tech": "services/digital-marketing_8PPCP5a.jpg",
        "Closing the Tech Skills Gap in Remote Teams": "services/project-management_9eVoEHy.jpg",
        "Why SEO-First Design is Crucial for 2024 Launch": "services/seo-audit_cwZznba.jpg",
        "Cybersecurity Best Practices for 2024": "services/web-development_8ihFnF4.jpg",
        "Improving User Retention Through Data Analytics": "services/ai-solutions_Sm4KGCl.jpg",
        "Streamlining Operations with Automation Tools": "services/project-management_9eVoEHy.jpg",
        "Content Strategy Trends for 2024": "services/content-production_Ydlk6M4.jpg",
        "Leveraging AI for Customer Support": "services/ai-solutions_Sm4KGCl.jpg",
        "Financial Planning for Growing Startups": "services/finance-accounting_2HYTx0j.jpg",
    }
    
    for post in blog_posts:
        if post.title in blog_image_mapping:
            image_path = blog_image_mapping[post.title]
            post.featured_image = image_path
            post.save()
            print(f"✓ {post.title[:50]}: {image_path}")
    
    print("\n✅ Blog images populated!")

def populate_testimonial_photos():
    """Add photos to testimonials"""
    print("\n\n=== Populating Testimonial Photos ===\n")
    
    testimonials = Testimonial.objects.all()
    
    # Use case study images for testimonial photos
    testimonial_image_mapping = {
        "Marcus Sterling": "case_studies/cloud-infrastructure.jpg",
    }
    
    for testimonial in testimonials:
        if testimonial.client_name in testimonial_image_mapping:
            image_path = testimonial_image_mapping[testimonial.client_name]
            testimonial.client_photo = image_path
            testimonial.save()
            print(f"✓ {testimonial.client_name}: {image_path}")
    
    print("\n✅ Testimonial photos populated!")

if __name__ == '__main__':
    populate_blog_images()
    populate_testimonial_photos()
