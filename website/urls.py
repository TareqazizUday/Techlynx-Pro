from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    
    # Full service URLs
    path('services/web-development/', views.web_development, name='web_development'),
    path('services/digital-marketing/', views.digital_marketing, name='digital_marketing'),
    path('services/ai-solutions/', views.ai_solutions, name='ai_solutions'),
    path('services/app-development/', views.app_development, name='app_development'),
    path('services/seo-audit/', views.seo_audit, name='seo_audit'),
    path('services/project-management/', views.project_management, name='project_management'),
    path('services/finance-accounting/', views.finance_accounting, name='finance_accounting'),
    path('services/content-production/', views.content_production, name='content_production'),
    path('services/virtual-assistance/', views.virtual_assistance, name='virtual_assistance'),
    
    path('industries/', views.industries, name='industries'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('case-studies/<slug:slug>/', views.case_study_detail, name='case_study_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/all/', views.all_blogs, name='all_blogs'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('careers/', views.careers, name='careers'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('api/chat/', views.chatbot_query, name='chatbot_query'),
]
