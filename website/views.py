from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import google.generativeai as genai
import json
import time
import requests
from .models import (
    ContactInquiry, Newsletter, HeroSection, HeroBenefit, CompanyStat,
    Service, Benefit, Guarantee, CaseStudy, Testimonial, Partner, CTASection,
    ServicesPageHero, ServiceDetail, WhyChooseItem, WhyChooseImage, ServicesPageCTA,
    SEOAuditHero, SEOAuditService, SEOAuditTool, SEOAuditToolLogo,
    SEOAuditProcess, SEOAuditResult, SEOAuditBenefit, SEOAuditHealthMetric,
    SEOAuditTestimonial, SEOAuditCTA,
    PMHero, PMService, PMTool, PMToolLogo, PMProcess, PMBenefit,
    PMMetric, PMTestimonial, PMCTA,
    FAHero, FAService, FATool, FAProcess, FABenefit, FATestimonial, FACTA,
    SEOAuditHero, SEOAuditService, SEOAuditTool, SEOAuditToolLogo,
    SEOAuditProcess, SEOAuditResult, SEOAuditBenefit, SEOAuditHealthMetric,
    SEOAuditTestimonial, SEOAuditCTA,
    AboutPageSEO, AboutPageHero, AboutPageMissionVision, AboutPageAdvantage,
    AboutPageAdvantageSection, AboutPageTimeline, AboutPageTimelineSection,
    AboutPageTeamMember, AboutPageTeamSection, AboutPageCTA
)
from .chatbot_context import get_chatbot_context

# Create your views here.

def home(request):
    """Homepage view with dynamic content"""
    context = {
        'hero_section': HeroSection.objects.first(),
        'hero_benefits': HeroBenefit.objects.all().order_by('order'),
        'stats': CompanyStat.objects.all().order_by('order'),
        'services': Service.objects.filter(is_active=True).order_by('order'),
        'benefits': Benefit.objects.all().order_by('order'),
        'guarantees': Guarantee.objects.all().order_by('order'),
        'featured_case_study': CaseStudy.objects.filter(is_featured=True).first(),
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('order'),
        'partners': Partner.objects.all().order_by('order'),
        'cta_section': CTASection.objects.first(),
    }
    return render(request, 'website/index.html', context)


def about(request):
    """About Us page view with dynamic content"""
    from .models import (
        AboutPageSEO, AboutPageHero, AboutPageMissionVision, AboutPageAdvantage,
        AboutPageAdvantageSection, AboutPageTimeline, AboutPageTimelineSection,
        AboutPageTeamMember, AboutPageTeamSection, AboutPageCTA
    )
    
    seo = AboutPageSEO.objects.first()
    hero = AboutPageHero.objects.filter(is_active=True).first()
    mission_vision = AboutPageMissionVision.objects.filter(is_active=True).first()
    advantage_section = AboutPageAdvantageSection.objects.filter(is_active=True).first()
    advantages = AboutPageAdvantage.objects.filter(is_active=True).order_by('order')
    timeline_section = AboutPageTimelineSection.objects.filter(is_active=True).first()
    timeline_items = AboutPageTimeline.objects.filter(is_active=True).order_by('order')
    team_section = AboutPageTeamSection.objects.filter(is_active=True).first()
    team_members = AboutPageTeamMember.objects.filter(is_active=True).order_by('order')
    cta = AboutPageCTA.objects.filter(is_active=True).first()
    
    context = {
        'seo': seo,
        'hero': hero,
        'mission_vision': mission_vision,
        'advantage_section': advantage_section,
        'advantages': advantages,
        'timeline_section': timeline_section,
        'timeline_items': timeline_items,
        'team_section': team_section,
        'team_members': team_members,
        'cta': cta,
    }
    
    return render(request, 'website/about.html', context)


def privacy_policy(request):
    """Privacy Policy page view with dynamic content"""
    from .models import PrivacyPolicy
    
    policy = PrivacyPolicy.objects.filter(is_active=True).first()
    
    context = {
        'policy': policy,
    }
    
    return render(request, 'website/privacy-policy.html', context)


def terms_of_service(request):
    """Terms of Service page view with dynamic content"""
    from .models import TermsOfService
    
    terms = TermsOfService.objects.filter(is_active=True).first()
    
    context = {
        'terms': terms,
    }
    
    return render(request, 'website/terms-of-service.html', context)


def services(request):
    """Services page view with dynamic content"""
    if request.method == 'POST':
        # Handle form submission
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        service_interest = request.POST.get('service_interest')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        budget_range = request.POST.get('budget_range', '')
        project_details = request.POST.get('project_details', f'Service inquiry for: {service_interest}')
        
        # Get tracking information
        source_url = request.POST.get('source_url', request.build_absolute_uri())
        referrer_url = request.META.get('HTTP_REFERER', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Get IP address (check for proxy/load balancer)
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR', None)
        if not ip_address or ip_address == '':
            ip_address = request.META.get('REMOTE_ADDR', None)
        
        # Get country from IP
        country = ''
        if ip_address:
            try:
                country = get_country_from_ip(ip_address)
            except:
                country = ''
        
        # Get UTM parameters if available
        utm_source = request.POST.get('utm_source', '')
        utm_medium = request.POST.get('utm_medium', '')
        utm_campaign = request.POST.get('utm_campaign', '')
        
        # Save inquiry to database
        if full_name and email and service_interest:
            ContactInquiry.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                company=company,
                service_interest=service_interest,
                budget_range=budget_range,
                project_details=project_details,
                source_url=source_url,
                referrer_url=referrer_url,
                user_agent=user_agent,
                ip_address=ip_address,
                country=country,
                utm_source=utm_source,
                utm_medium=utm_medium,
                utm_campaign=utm_campaign,
            )
            messages.success(request, 'Thank you! Your inquiry has been submitted successfully. We will contact you soon.')
        else:
            messages.error(request, 'Please fill in all required fields.')
        
        return redirect('services')
    
    context = {
        'hero': ServicesPageHero.objects.first(),
        'services': ServiceDetail.objects.filter(is_active=True).prefetch_related('features').order_by('order'),
        'why_choose_items': WhyChooseItem.objects.filter(is_active=True).order_by('order'),
        'why_choose_images': WhyChooseImage.objects.filter(is_active=True).order_by('order')[:4],  # Limit to 4 active images for 2x2 grid
        'cta_section': ServicesPageCTA.objects.filter(is_active=True).prefetch_related('checklist_items').first(),
    }
    return render(request, 'website/services.html', context)


def web_development(request):
    """Web Development services page"""
    from .models import (
        WebDevHero, WebDevService, WebDevStackFeature, WebDevTechnology,
        WebDevProcess, WebDevSEOBenefit, WebDevSEOMetric, WebDevCTA
    )
    
    context = {
        'hero': WebDevHero.objects.filter(is_active=True).first(),
        'services': WebDevService.objects.filter(is_active=True),
        'stack_features': WebDevStackFeature.objects.filter(is_active=True),
        'technologies': WebDevTechnology.objects.filter(is_active=True),
        'process_steps': WebDevProcess.objects.filter(is_active=True),
        'seo_benefits': WebDevSEOBenefit.objects.filter(is_active=True),
        'seo_metrics': WebDevSEOMetric.objects.filter(is_active=True),
        'cta': WebDevCTA.objects.filter(is_active=True).first(),
    }
    
    return render(request, 'website/web-development.html', context)


def digital_marketing(request):
    """Digital Marketing services page"""
    from .models import (
        DigitalMarketingHero, DigitalMarketingService, DigitalMarketingStrategy,
        DigitalMarketingTestimonial, DigitalMarketingMetric, DigitalMarketingCTA
    )
    
    context = {
        'hero': DigitalMarketingHero.objects.filter(is_active=True).first(),
        'services': DigitalMarketingService.objects.filter(is_active=True),
        'strategy_steps': DigitalMarketingStrategy.objects.filter(is_active=True),
        'testimonials': DigitalMarketingTestimonial.objects.filter(is_active=True),
        'metrics': DigitalMarketingMetric.objects.filter(is_active=True),
        'cta': DigitalMarketingCTA.objects.filter(is_active=True).first(),
    }
    
    return render(request, 'website/digital-marketing.html', context)


def ai_solutions(request):
    """AI Solutions services page with dynamic content"""
    from .models import (
        AISolutionsHero, AIService, AITechnology, AITechnologyDetail,
        AIImplementationStep, AIROIMetric, AIPerformanceMetric,
        AITestimonial, AISolutionsCTA
    )
    
    context = {
        'hero': AISolutionsHero.objects.filter(is_active=True).first(),
        'ai_services': AIService.objects.filter(is_active=True).order_by('order'),
        'ai_technologies': AITechnology.objects.filter(is_active=True).order_by('order'),
        'tech_details': AITechnologyDetail.objects.filter(is_active=True).order_by('order'),
        'implementation_steps': AIImplementationStep.objects.filter(is_active=True).order_by('order'),
        'roi_metrics': AIROIMetric.objects.filter(is_active=True).order_by('order'),
        'performance_metrics': AIPerformanceMetric.objects.filter(is_active=True).order_by('order'),
        'ai_testimonials': AITestimonial.objects.filter(is_active=True).order_by('order'),
        'cta_section': AISolutionsCTA.objects.filter(is_active=True).first(),
    }
    return render(request, 'website/ai-solutions.html', context)


def app_development(request):
    """App Development services page"""
    from .models import (
        AppDevHero, AppDevService, AppDevStackFeature, AppDevTechnology,
        AppDevProcess, AppDevFeature, AppDevPerformanceMetric,
        AppDevTestimonial, AppDevCTA
    )
    
    context = {
        'hero': AppDevHero.objects.filter(is_active=True).first(),
        'services': AppDevService.objects.filter(is_active=True),
        'stack_features': AppDevStackFeature.objects.filter(is_active=True),
        'technologies': AppDevTechnology.objects.filter(is_active=True),
        'process_steps': AppDevProcess.objects.filter(is_active=True),
        'features': AppDevFeature.objects.filter(is_active=True),
        'performance_metrics': AppDevPerformanceMetric.objects.filter(is_active=True),
        'testimonials': AppDevTestimonial.objects.filter(is_active=True),
        'cta': AppDevCTA.objects.filter(is_active=True).first(),
    }
    
    return render(request, 'website/app-development.html', context)


def seo_audit(request):
    """SEO Audit services page with dynamic content"""
    context = {
        'hero': SEOAuditHero.objects.filter(is_active=True).first(),
        'seo_services': SEOAuditService.objects.filter(is_active=True).order_by('order'),
        'seo_tools': SEOAuditTool.objects.filter(is_active=True).order_by('order'),
        'tool_logos': SEOAuditToolLogo.objects.filter(is_active=True).order_by('order'),
        'process_steps': SEOAuditProcess.objects.filter(is_active=True).order_by('step_number'),
        'results': SEOAuditResult.objects.filter(is_active=True).first(),
        'benefits': SEOAuditBenefit.objects.filter(is_active=True).order_by('order'),
        'health_metrics': SEOAuditHealthMetric.objects.filter(is_active=True).order_by('order'),
        'testimonials': SEOAuditTestimonial.objects.filter(is_active=True).order_by('order'),
        'cta_section': SEOAuditCTA.objects.filter(is_active=True).first(),
    }
    return render(request, 'website/seo-audit.html', context)


def project_management(request):
    """Project Management services page"""
    context = {
        'hero': PMHero.objects.filter(is_active=True).first(),
        'services': PMService.objects.filter(is_active=True).order_by('order'),
        'tools': PMTool.objects.filter(is_active=True).order_by('order'),
        'tool_logos': PMToolLogo.objects.filter(is_active=True).order_by('order'),
        'process_steps': PMProcess.objects.filter(is_active=True).order_by('step_number'),
        'benefits': PMBenefit.objects.filter(is_active=True).order_by('order'),
        'metrics': PMMetric.objects.filter(is_active=True).order_by('order'),
        'testimonials': PMTestimonial.objects.filter(is_active=True).order_by('order'),
        'cta': PMCTA.objects.filter(is_active=True).first(),
    }
    return render(request, 'website/project-management.html', context)



def finance_accounting(request):
    """Finance & Accounting services page"""
    context = {
        'hero': FAHero.objects.filter(is_active=True).first(),
        'services': FAService.objects.filter(is_active=True).order_by('order'),
        'tools': FATool.objects.filter(is_active=True).order_by('order'),
        'process_steps': FAProcess.objects.filter(is_active=True).order_by('order'),
        'benefits': FABenefit.objects.filter(is_active=True).order_by('order'),
        'testimonials': FATestimonial.objects.filter(is_active=True).order_by('order'),
        'cta': FACTA.objects.filter(is_active=True).first(),
    }
    return render(request, 'website/finance-accounting.html', context)


def content_production(request):
    """Content Production & Creative services page"""
    from .models import CPService, CPTool, CPBenefit, CPProcessStep, CPMetric, CPTestimonial, CPTechnology
    
    context = {
        'services': CPService.objects.filter(is_active=True),
        'tools': CPTool.objects.filter(is_active=True),
        'technologies': CPTechnology.objects.filter(is_active=True),
        'benefits': CPBenefit.objects.filter(is_active=True),
        'process_steps': CPProcessStep.objects.filter(is_active=True),
        'metrics': CPMetric.objects.filter(is_active=True),
        'testimonials': CPTestimonial.objects.filter(is_active=True),
    }
    return render(request, 'website/content-production.html', context)


def virtual_assistance(request):
    """Virtual Assistance services page"""
    from .models import VAHero, VAService, VABenefit, VACTA
    
    context = {
        'hero': VAHero.objects.filter(is_active=True).first(),
        'services': VAService.objects.filter(is_active=True).order_by('order'),
        'benefits': VABenefit.objects.filter(is_active=True).order_by('order'),
        'cta': VACTA.objects.filter(is_active=True).first(),
    }
    
    return render(request, 'website/virtual-assistance.html', context)


def industries(request):
    """Industries We Serve page"""
    return render(request, 'website/industries.html')


def case_studies(request):
    """Case Studies page with dynamic content and filtering"""
    # Get filter parameters from URL
    category_filter = request.GET.get('category', 'all')
    sort_by = request.GET.get('sort', 'latest')
    
    # Start with all active case studies
    case_studies = CaseStudy.objects.filter(is_active=True)
    
    # Apply category filter
    if category_filter and category_filter != 'all':
        case_studies = case_studies.filter(category=category_filter)
    
    # Apply sorting
    if sort_by == 'latest':
        case_studies = case_studies.order_by('-created_at')
    elif sort_by == 'impact':
        case_studies = case_studies.order_by('order')  # Assuming lower order = higher impact
    elif sort_by == 'industry':
        case_studies = case_studies.order_by('category', '-created_at')
    else:
        case_studies = case_studies.order_by('order')
    
    # Get unique categories for filters
    categories = CaseStudy.objects.filter(is_active=True).values_list('category', flat=True).distinct().order_by('category')
    
    context = {
        'case_studies': case_studies,
        'categories': categories,
        'active_category': category_filter,
        'active_sort': sort_by,
    }
    return render(request, 'website/case-studies.html', context)


def case_study_detail(request, slug):
    """Individual case study detail page"""
    case_study = CaseStudy.objects.filter(slug=slug, is_active=True).first()
    
    if not case_study:
        from django.http import Http404
        raise Http404("Case study not found")
    
    # Get related case studies from same category
    related_case_studies = CaseStudy.objects.filter(
        category=case_study.category,
        is_active=True
    ).exclude(id=case_study.id).order_by('order')[:3]
    
    # Get CTA content
    from .models import CaseStudiesPageCTA
    cta = CaseStudiesPageCTA.objects.filter(is_active=True).first()
    
    context = {
        'case_study': case_study,
        'related_case_studies': related_case_studies,
        'cta': cta,
    }
    return render(request, 'website/case-study-detail.html', context)


def blog(request):
    """Blog/Insights page"""
    from .models import BlogCategory, BlogPost
    
    # Get active categories ordered by custom order
    categories = BlogCategory.objects.filter(is_active=True).order_by('order')
    
    # Get featured post for hero section
    featured_post = BlogPost.objects.filter(
        is_featured=True, 
        is_published=True
    ).first()
    
    # Get trending posts for sidebar (max 3)
    trending_posts = BlogPost.objects.filter(
        is_trending=True,
        is_published=True
    ).select_related('category').order_by('trending_order')[:3]
    
    # Get regular posts (excluding featured) - limit to 8
    posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(
        is_featured=True
    ).select_related('category').order_by('-published_date')[:8]
    
    # Check if there are more posts
    total_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(
        is_featured=True
    ).count()
    
    context = {
        'categories': categories,
        'featured_post': featured_post,
        'trending_posts': trending_posts,
        'posts': posts,
        'has_more_posts': total_posts > 8,
    }
    
    return render(request, 'website/blog.html', context)


def all_blogs(request):
    """All blogs page - shows all published blog posts"""
    from .models import BlogCategory, BlogPost
    
    # Get active categories ordered by custom order
    categories = BlogCategory.objects.filter(is_active=True).order_by('order')
    
    # Get featured post for hero section
    featured_post = BlogPost.objects.filter(
        is_featured=True, 
        is_published=True
    ).first()
    
    # Get trending posts for sidebar (max 3)
    trending_posts = BlogPost.objects.filter(
        is_trending=True,
        is_published=True
    ).select_related('category').order_by('trending_order')[:3]
    
    # Get ALL published posts (including featured)
    posts = BlogPost.objects.filter(
        is_published=True
    ).select_related('category').order_by('-published_date')
    
    # Count posts by category for meta description
    total_posts = posts.count()
    
    context = {
        'categories': categories,
        'featured_post': featured_post,
        'trending_posts': trending_posts,
        'posts': posts,
        'show_all': True,
        'page_title': f'All Blog Articles & Insights ({total_posts}+) | Tech Trends & Expert Tips',
        'meta_description': f'Browse all {total_posts}+ articles on web development, AI automation, digital marketing, SEO, and technology trends. Comprehensive industry insights, tutorials, case studies, and best practices from Techlynx experts. Find solutions to your tech challenges.',
    }
    
    return render(request, 'website/blog.html', context)


def blog_detail(request, slug):
    """Individual blog post detail page"""
    from .models import BlogPost, BlogCategory
    
    # Get the blog post by slug
    post = BlogPost.objects.select_related('category').filter(
        slug=slug,
        is_published=True
    ).first()
    
    if not post:
        from django.http import Http404
        raise Http404("Blog post not found")
    
    # Get related posts (same category, excluding current post)
    related_posts = BlogPost.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id).select_related('category')[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'website/blog_detail.html', context)


def careers(request):
    """Careers page with dynamic content and application form handling"""
    from .models import (CareersHero, CareersStat, JobDepartment, JobLocation,
                        JobOpening, TalentManagement, TalentFeature, CareerApplication)
    
    # Handle form submission
    if request.method == 'POST':
        try:
            application = CareerApplication()
            application.full_name = request.POST.get('full_name')
            application.email = request.POST.get('email')
            application.application_type = request.POST.get('interest')
            application.links = request.POST.get('links', '')
            
            # Get job position if provided
            job_id = request.POST.get('job_position')
            if job_id:
                try:
                    application.job_position = JobOpening.objects.get(id=job_id)
                except JobOpening.DoesNotExist:
                    pass
            
            # Handle file upload
            if 'resume' in request.FILES:
                application.resume = request.FILES['resume']
            
            application.save()
            messages.success(request, 'Your application has been submitted successfully! We will get back to you soon.')
            return redirect('careers')
        except Exception as e:
            messages.error(request, 'There was an error submitting your application. Please try again.')
    
    # Get job_id from URL parameter if provided
    job_id = request.GET.get('job')
    selected_job = None
    if job_id:
        try:
            selected_job = JobOpening.objects.get(id=job_id, is_active=True)
        except JobOpening.DoesNotExist:
            pass
    
    context = {
        'hero': CareersHero.objects.filter(is_active=True).first(),
        'stats': CareersStat.objects.filter(is_active=True).order_by('order'),
        'departments': JobDepartment.objects.filter(is_active=True).order_by('order'),
        'locations': JobLocation.objects.filter(is_active=True).order_by('order'),
        'job_openings': JobOpening.objects.filter(is_active=True).select_related('department', 'location').order_by('order'),
        'talent_management': TalentManagement.objects.filter(is_active=True).first(),
        'talent_features': TalentFeature.objects.filter(is_active=True).order_by('order'),
        'selected_job': selected_job,
    }
    
    return render(request, 'website/careers.html', context)


def testimonials(request):
    """Testimonials page showcasing client reviews from all services"""
    from .models import (
        AITestimonial, DigitalMarketingTestimonial, AppDevTestimonial,
        SEOAuditTestimonial, PMTestimonial, FATestimonial, CPTestimonial,
        TestimonialsPageSEO, TestimonialsPageHero, TestimonialsPageWhyChoose,
        TestimonialsPageWhyChooseReason, TestimonialsPageCTA, TestimonialsPageMetric
    )
    
    # Get dynamic page content
    seo = TestimonialsPageSEO.objects.first()
    hero = TestimonialsPageHero.objects.filter(is_active=True).first()
    why_choose = TestimonialsPageWhyChoose.objects.filter(is_active=True).first()
    why_choose_reasons = TestimonialsPageWhyChooseReason.objects.filter(is_active=True).order_by('order')
    cta = TestimonialsPageCTA.objects.filter(is_active=True).first()
    metrics = TestimonialsPageMetric.objects.filter(is_active=True).order_by('order')
    
    # Gather testimonials from all services
    ai_testimonials = AITestimonial.objects.filter(is_active=True).order_by('order')[:10]
    marketing_testimonials = DigitalMarketingTestimonial.objects.filter(is_active=True).order_by('order')[:10]
    app_testimonials = AppDevTestimonial.objects.filter(is_active=True).order_by('order')[:10]
    seo_testimonials = SEOAuditTestimonial.objects.filter(is_active=True).order_by('order')[:10]
    pm_testimonials = PMTestimonial.objects.filter(is_active=True).order_by('order')[:10]
    fa_testimonials = FATestimonial.objects.filter(is_active=True).order_by('order')[:10]
    cp_testimonials = CPTestimonial.objects.filter(is_active=True).order_by('order')[:10]
    
    # Create unified testimonial list with service metadata for simplified templating
    unified_testimonials = []
    
    # AI Solutions (Blue theme)
    for testimonial in ai_testimonials:
        unified_testimonials.append({
            'testimonial': testimonial,
            'service': 'AI Solutions',
            'color_primary': 'primary',
            'color_secondary': 'blue-600',
            'bg_gradient_from': 'blue-500/10',
            'bg_gradient_to': 'purple-500/10',
            'border_color': 'blue-200',
            'dark_border': 'blue-800',
            'text_color': 'blue-600',
            'dark_text': 'blue-400'
        })
    
    # Digital Marketing (Green theme)
    for testimonial in marketing_testimonials:
        unified_testimonials.append({
            'testimonial': testimonial,
            'service': 'Digital Marketing',
            'color_primary': 'green-500',
            'color_secondary': 'emerald-600',
            'bg_gradient_from': 'green-500/10',
            'bg_gradient_to': 'emerald-500/10',
            'border_color': 'green-200',
            'dark_border': 'green-800',
            'text_color': 'green-600',
            'dark_text': 'green-400'
        })
    
    # App Development (Purple theme)
    for testimonial in app_testimonials:
        unified_testimonials.append({
            'testimonial': testimonial,
            'service': 'App Development',
            'color_primary': 'purple-500',
            'color_secondary': 'pink-600',
            'bg_gradient_from': 'purple-500/10',
            'bg_gradient_to': 'pink-500/10',
            'border_color': 'purple-200',
            'dark_border': 'purple-800',
            'text_color': 'purple-600',
            'dark_text': 'purple-400'
        })
    
    # Calculate total testimonials
    total_testimonials = (
        ai_testimonials.count() + marketing_testimonials.count() + 
        app_testimonials.count() + seo_testimonials.count() + 
        pm_testimonials.count() + fa_testimonials.count() + 
        cp_testimonials.count()
    )
    
    context = {
        # Dynamic page content
        'seo': seo,
        'hero': hero,
        'why_choose': why_choose,
        'why_choose_reasons': why_choose_reasons,
        'cta': cta,
        'metrics': metrics,
        # Unified testimonials (removes duplicate template code)
        'unified_testimonials': unified_testimonials,
        # Legacy testimonials (kept for compatibility)
        'ai_testimonials': ai_testimonials,
        'marketing_testimonials': marketing_testimonials,
        'app_testimonials': app_testimonials,
        'seo_testimonials': seo_testimonials,
        'pm_testimonials': pm_testimonials,
        'fa_testimonials': fa_testimonials,
        'cp_testimonials': cp_testimonials,
        'total_testimonials': total_testimonials,
    }
    
    return render(request, 'website/testimonials.html', context)


def get_country_from_ip(ip_address):
    """Get country name from IP address using free API"""
    if not ip_address:
        return 'Unknown'
    
    # Check for local/private IPs
    if ip_address == '127.0.0.1' or ip_address == '::1' or ip_address.startswith('192.168.') or ip_address.startswith('10.') or ip_address.startswith('172.16.'):
        return 'Local/Unknown'
    
    # Try multiple APIs to get country
    try:
        # Method 1: ip-api.com (free, no API key required, 45 requests/minute)
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                country = data.get('country', '').strip()
                if country and country != 'None':
                    return country
    except Exception as e:
        pass
    
    try:
        # Method 2: ipapi.co (free, 1000 requests/day)
        response = requests.get(f'https://ipapi.co/{ip_address}/country_name/', timeout=5)
        if response.status_code == 200:
            country = response.text.strip()
            if country and country != 'None' and country != 'Undefined':
                return country
    except Exception as e:
        pass
    
    try:
        # Method 3: ip-api.com alternative endpoint
        response = requests.get(f'https://ip-api.com/json/{ip_address}?fields=status,country', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                country = data.get('country', '').strip()
                if country and country != 'None':
                    return country
    except Exception as e:
        pass
    
    try:
        # Method 4: ipgeolocation.io (free tier available)
        response = requests.get(f'https://api.ipgeolocation.io/ipgeo?ip={ip_address}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            country = data.get('country_name', '').strip()
            if country and country != 'None':
                return country
    except Exception as e:
        pass
    
    # If all APIs fail, return Unknown
    return 'Unknown'

def contact(request):
    """Contact page with form handling and tracking"""
    if request.method == 'POST':
        try:
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            # Get country from IP address
            country = get_country_from_ip(ip_address) if ip_address else 'Unknown'
            
            # Save contact inquiry with tracking information
            inquiry = ContactInquiry(
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone', ''),
                company=request.POST.get('company', ''),
                service_interest=request.POST.get('service_interest'),
                budget_range=request.POST.get('budget_range', ''),
                project_details=request.POST.get('project_details', ''),
                # Tracking fields
                source_url=request.POST.get('source_url', request.build_absolute_uri()),
                referrer_url=request.META.get('HTTP_REFERER', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=ip_address,
                country=country,
                utm_source=request.POST.get('utm_source', ''),
                utm_medium=request.POST.get('utm_medium', ''),
                utm_campaign=request.POST.get('utm_campaign', ''),
            )
            inquiry.save()
            messages.success(request, 'Thank you! Your inquiry has been submitted successfully. We will get back to you within 24 hours.')
            return redirect('contact')
        except Exception as e:
            messages.error(request, f'An error occurred. Please try again. Error: {str(e)}')
    
    # Get current URL and UTM parameters for form
    context = {
        'current_url': request.build_absolute_uri(),
        'utm_source': request.GET.get('utm_source', ''),
        'utm_medium': request.GET.get('utm_medium', ''),
        'utm_campaign': request.GET.get('utm_campaign', ''),
        'referrer': request.META.get('HTTP_REFERER', ''),
    }
    
    return render(request, 'website/contact.html', context)


def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Please provide a valid email address.'}, status=400)
            messages.error(request, 'Please provide a valid email address.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        try:
            # Check if email already exists
            if Newsletter.objects.filter(email=email).exists():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'This email is already subscribed to our newsletter.'}, status=400)
                messages.info(request, 'This email is already subscribed to our newsletter.')
            else:
                Newsletter.objects.create(email=email)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Successfully subscribed to our newsletter! Thank you!'})
                messages.success(request, 'Successfully subscribed to our newsletter! Thank you!')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'An error occurred. Please try again later.'}, status=500)
            messages.error(request, 'An error occurred. Please try again later.')
    
    # Redirect to referer or home
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


@csrf_exempt
def chatbot_query(request):
    """Handle chatbot queries using Gemini API"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Parse request body
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        # Validate input
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        if len(user_message) > 500:
            return JsonResponse({'error': 'Message too long (max 500 characters)'}, status=400)
        
        # Check rate limiting (session-based)
        if 'chatbot_queries' not in request.session:
            request.session['chatbot_queries'] = []
        
        # Clean up old queries (older than 1 hour)
        current_time = time.time()
        request.session['chatbot_queries'] = [
            t for t in request.session['chatbot_queries'] 
            if current_time - t < 3600
        ]
        
        # Check if user exceeded limit (10 queries per hour)
        if len(request.session['chatbot_queries']) >= 10:
            return JsonResponse({
                'error': 'Rate limit exceeded. Please try again later.',
                'status': 'rate_limited'
            }, status=429)
        
        # Add current query timestamp
        request.session['chatbot_queries'].append(current_time)
        request.session.modified = True
        
        # Get API key from settings
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return JsonResponse({
                'error': 'Chatbot is temporarily unavailable',
                'status': 'error'
            }, status=503)
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Get site context
        site_context = get_chatbot_context()
        
        # Build system prompt
        system_prompt = f"""You are a helpful AI assistant for Techlynx Pro, a professional IT services company based in the United States.

Your role:
- Answer questions about Techlynx Pro's services, pricing, company information, and expertise
- Be professional, friendly, and conversion-focused
- Encourage users to contact the company for specific project quotes and detailed consultations
- Only provide information based on the context provided below
- If you don't have specific information, politely say so and suggest contacting the team directly

IMPORTANT GUIDELINES:
- Do NOT discuss competitors or make comparisons
- Do NOT provide exact pricing without context (mention ranges and encourage contact)
- Do NOT make promises on behalf of the company
- Keep responses concise (2-3 paragraphs maximum)
- Always maintain a helpful and professional tone
- Use bullet points for listing services or features for better readability

COMPANY CONTEXT:
{site_context}

User Question: {user_message}

Provide a helpful, accurate response based on the context above:"""
        
        # Generate response
        response = model.generate_content(system_prompt)
        bot_response = response.text
        
        return JsonResponse({
            'response': bot_response,
            'status': 'success'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Chatbot error: {e}")
        return JsonResponse({
            'error': 'Sorry, I encountered an error. Please try again.',
            'status': 'error'
        }, status=500)
