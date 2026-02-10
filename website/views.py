from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import google.generativeai as genai
import json
import time
from .models import ContactInquiry, Newsletter
from .chatbot_context import get_chatbot_context

# Create your views here.

def home(request):
    """Homepage view"""
    return render(request, 'website/index.html')


def about(request):
    """About Us page view"""
    return render(request, 'website/about.html')


def services(request):
    """Services page view"""
    return render(request, 'website/services.html')


def web_development(request):
    """Web Development services page"""
    return render(request, 'website/web-development.html')


def digital_marketing(request):
    """Digital Marketing services page"""
    return render(request, 'website/digital-marketing.html')


def ai_solutions(request):
    """AI Solutions services page"""
    return render(request, 'website/ai-solutions.html')


def app_development(request):
    """App Development services page"""
    return render(request, 'website/app-development.html')


def seo_audit(request):
    """SEO Audit services page"""
    return render(request, 'website/seo-audit.html')


def project_management(request):
    """Project Management services page"""
    return render(request, 'website/project-management.html')


def finance_accounting(request):
    """Finance & Accounting services page"""
    return render(request, 'website/finance-accounting.html')


def content_production(request):
    """Content Production & Creative services page"""
    return render(request, 'website/content-production.html')


def industries(request):
    """Industries We Serve page"""
    return render(request, 'website/industries.html')


def case_studies(request):
    """Case Studies page"""
    return render(request, 'website/case-studies.html')


def blog(request):
    """Blog/Insights page"""
    return render(request, 'website/blog.html')


def careers(request):
    """Careers page"""
    return render(request, 'website/careers.html')


def contact(request):
    """Contact page with form handling"""
    if request.method == 'POST':
        try:
            # Save contact inquiry
            inquiry = ContactInquiry(
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                service_interest=request.POST.get('service_interest'),
                budget_range=request.POST.get('budget_range', ''),
                project_details=request.POST.get('project_details', '')
            )
            inquiry.save()
            messages.success(request, 'Thank you! Your inquiry has been submitted successfully.')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again.')
    
    return render(request, 'website/contact.html')


def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            Newsletter.objects.create(email=email)
            messages.success(request, 'Successfully subscribed to our newsletter!')
        except:
            messages.info(request, 'This email is already subscribed.')
    
    return redirect('home')


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
