from django.db import models

# Create your models here.

class ContactInquiry(models.Model):
    """Model to store contact form submissions"""
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    service_interest = models.CharField(max_length=100)
    budget_range = models.CharField(max_length=50, blank=True)
    project_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Contact Form Submission'
        verbose_name_plural = '📧 Contact Forms'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.email}"


class Newsletter(models.Model):
    """Model to store newsletter subscriptions"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = '📧 Newsletter Subscribers'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


# ==================== HOME PAGE DYNAMIC CONTENT MODELS ====================

class HeroSection(models.Model):
    """Main hero section content (singleton - only one record should exist)"""
    headline = models.CharField(max_length=200, help_text="Main headline text")
    subheadline = models.TextField(help_text="Subheadline description")
    cta_primary_text = models.CharField(max_length=100, default="Get Free Strategy Call")
    cta_primary_url = models.CharField(max_length=200, default="#contact")
    cta_secondary_text = models.CharField(max_length=100, default="Success Stories")
    cta_secondary_url = models.CharField(max_length=200, default="/case-studies")
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True, 
                                   help_text="Hero section image (right side visual)")
    rating_score = models.DecimalField(max_digits=2, decimal_places=1, default=4.9,
                                      help_text="Client rating score (e.g., 4.9)")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '1️⃣ Hero Section'
        verbose_name_plural = '1️⃣ Hero Section (Main Banner)'
    
    def __str__(self):
        return "Hero Section Content"


class HeroBenefit(models.Model):
    """Key benefits displayed in hero section (e.g., 200% AVG ROI)"""
    title = models.CharField(max_length=100, help_text="Benefit title (e.g., AVG ROI)")
    value = models.CharField(max_length=50, help_text="Benefit value (e.g., 200%)")
    icon = models.CharField(max_length=100, default="trending_up",
                           help_text="Material icon name")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        verbose_name = '2️⃣ Hero Benefit'
        verbose_name_plural = '2️⃣ Hero Benefits (Key Metrics)'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.value} {self.title}"


class CompanyStat(models.Model):
    """Company statistics section (e.g., 500+ Projects Delivered)"""
    label = models.CharField(max_length=100, help_text="Stat label")
    value = models.CharField(max_length=50, help_text="Stat value (e.g., 500+)")
    icon = models.CharField(max_length=100, default="check_circle",
                           help_text="Material icon name")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        verbose_name = '5️⃣ Company Statistic'
        verbose_name_plural = '5️⃣ Company Statistics'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.value} {self.label}"


class Service(models.Model):
    """Service cards displayed on home page"""
    title = models.CharField(max_length=100)
    description = models.TextField(help_text="Service description with key benefits")
    icon = models.CharField(max_length=100, default="settings",
                           help_text="Material icon name (fallback if no image)")
    image = models.FileField(upload_to='services/', null=True, blank=True,
                         help_text="SVG service icon")
    detail_page_url = models.CharField(max_length=200, 
                                       help_text="URL slug (e.g., /services/ai-solutions/)")
    is_active = models.BooleanField(default=True, help_text="Show on home page")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        verbose_name = '0️⃣ Service'
        verbose_name_plural = '0️⃣ Services (Home Page Cards)'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Benefit(models.Model):
    """Why Choose Us benefits"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, default="verified",
                           help_text="Material icon name")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        verbose_name = '6️⃣ Benefit'
        verbose_name_plural = '6️⃣ Benefits (Why Choose Us)'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Guarantee(models.Model):
    """Our Guarantees items"""
    text = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, default="shield",
                           help_text="Material icon name")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        verbose_name = '7️⃣ Guarantee'
        verbose_name_plural = '7️⃣ Guarantees (Our Guarantees)'
        ordering = ['order']
    
    def __str__(self):
        return self.text


class CaseStudy(models.Model):
    """Featured case studies/client transformations"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, 
                           help_text="URL-friendly version (auto-generated)")
    category = models.CharField(max_length=100, help_text="E.g., E-commerce, SaaS, Healthcare, Logistics")
    description = models.TextField(help_text="Short description for card")
    detailed_description = models.TextField(blank=True, 
                                           help_text="Full detailed description for detail page")
    client_name = models.CharField(max_length=200, blank=True, 
                                  help_text="Client company name (optional)")
    challenge = models.TextField(blank=True, help_text="The challenge/problem")
    solution = models.TextField(blank=True, help_text="Our solution")
    results = models.TextField(blank=True, help_text="Results achieved")
    background_image = models.ImageField(upload_to='case_studies/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=200, blank=True, 
                                     help_text="SEO-friendly alt text for the image")
    key_result_label = models.CharField(max_length=100, default="Key Result",
                                       help_text="E.g., Key Result, User Engagement, Ad Spend")
    key_result_value = models.CharField(max_length=100, default="+100%",
                                       help_text="E.g., 45% Ops Reduction, +150% Growth, 3.5x ROI")
    is_active = models.BooleanField(default=True, 
                                   help_text="Show on case studies page")
    is_featured = models.BooleanField(default=False, 
                                     help_text="Show as featured on home page")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '8️⃣ Case Study'
        verbose_name_plural = '8️⃣ Case Studies (Success Stories)'
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/case-studies/{self.slug}/'


class CaseStudyMetric(models.Model):
    """Metrics for case studies (e.g., 340% Organic Traffic)"""
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, 
                                   related_name='metrics')
    label = models.CharField(max_length=100, help_text="E.g., Organic Traffic")
    value = models.CharField(max_length=50, help_text="E.g., 340%")
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Case Study Metric'
        verbose_name_plural = 'Case Study Metrics'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.value} {self.label}"


class CaseStudiesPageCTA(models.Model):
    """CTA section for case study detail pages"""
    headline = models.CharField(max_length=200, default="Ready for Similar Results?",
                               help_text="Main CTA headline")
    description = models.TextField(default="Let's discuss how we can help transform your business with proven strategies and solutions.",
                                  help_text="CTA description text")
    primary_button_text = models.CharField(max_length=50, default="Start Your Project",
                                         help_text="Primary button text")
    primary_button_url = models.CharField(max_length=200, default="/contact/",
                                        help_text="Primary button URL")
    secondary_button_text = models.CharField(max_length=50, default="View More Case Studies",
                                           help_text="Secondary button text")
    secondary_button_url = models.CharField(max_length=200, default="/case-studies/",
                                          help_text="Secondary button URL")
    is_active = models.BooleanField(default=True,
                                   help_text="Show this CTA on case study detail pages")
    
    class Meta:
        verbose_name = 'Case Study Page CTA'
        verbose_name_plural = 'Case Study Page CTA'
    
    def __str__(self):
        return self.headline
    
    def save(self, *args, **kwargs):
        # Only allow one active CTA
        if self.is_active:
            CaseStudiesPageCTA.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    """Client testimonials"""
    client_name = models.CharField(max_length=100)
    client_title = models.CharField(max_length=100, help_text="E.g., CEO")
    client_company = models.CharField(max_length=200)
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    quote = models.TextField(help_text="Client testimonial quote")
    rating = models.IntegerField(default=5, help_text="Star rating (1-5)")
    is_active = models.BooleanField(default=True, help_text="Show on home page")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '9️⃣ Testimonial'
        verbose_name_plural = '9️⃣ Testimonials (Client Reviews)'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class Partner(models.Model):
    """Trusted by / Partner logos"""
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='partners/', help_text="Partner SVG logo file")
    website_url = models.URLField(blank=True, help_text="Partner website (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        verbose_name = '3️⃣ Partner Logo'
        verbose_name_plural = '3️⃣ Partner Logos (Trusted By)'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class CTASection(models.Model):
    """Final Call-to-Action section (singleton - only one record should exist)"""
    headline = models.CharField(max_length=200)
    description = models.TextField()
    button_primary_text = models.CharField(max_length=100)
    button_primary_url = models.CharField(max_length=200)
    button_secondary_text = models.CharField(max_length=100, blank=True)
    button_secondary_url = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '🔟 CTA Section'
        verbose_name_plural = '🔟 CTA Section (Call-to-Action)'
    
    def __str__(self):
        return "CTA Section Content"


# ==================== SERVICES PAGE DYNAMIC CONTENT MODELS ====================

class ServicesPageHero(models.Model):
    """Services page hero section (singleton - only one record should exist)"""
    badge_text = models.CharField(max_length=100, default="Trusted US-Based Agency",
                                  help_text="Top badge text")
    headline = models.CharField(max_length=200, 
                               default="Scalable IT & Digital Marketing Solutions")
    subheadline = models.TextField(
        default="High-performance expertise to help your business dominate the market")
    cta_primary_text = models.CharField(max_length=100, default="View Our Services")
    cta_primary_url = models.CharField(max_length=200, default="#services")
    cta_secondary_text = models.CharField(max_length=100, default="Talk to an Expert")
    cta_secondary_url = models.CharField(max_length=200, default="/contact")
    hero_image = models.ImageField(upload_to='services/hero/', blank=True, null=True,
                                   help_text="Hero section background image")
    stat_value = models.CharField(max_length=50, default="98%",
                                  help_text="Stat badge value (e.g., 98%)")
    stat_label = models.CharField(max_length=100, default="Client Success Rate",
                                  help_text="Stat badge label")
    stat_icon = models.CharField(max_length=100, default="trending_up",
                                help_text="Material icon name for stat badge")
    is_stat_visible = models.BooleanField(default=True,
                                         help_text="Show/hide stat badge")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '1️⃣ Services Hero'
        verbose_name_plural = '1️⃣ Services Hero Section'
    
    def __str__(self):
        return "Services Hero Section"


class ServiceDetail(models.Model):
    """Individual service cards on services page"""
    title = models.CharField(max_length=100, help_text="Service name (e.g., AI Solutions)")
    description = models.TextField(help_text="Service description paragraph")
    icon = models.CharField(max_length=100, default="settings",
                           help_text="Material Symbols icon name (fallback if no image)")
    image = models.FileField(upload_to='services/', null=True, blank=True,
                         help_text="SVG service icon")
    detail_page_url = models.CharField(max_length=200,
                                       help_text="Detail page URL (e.g., /services/ai-solutions/)")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    is_active = models.BooleanField(default=True, help_text="Show on services page")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '2️⃣ Service Detail'
        verbose_name_plural = '2️⃣ Service Details (Service Cards)'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    """Features/bullet points for each service"""
    service = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE,
                               related_name='features')
    feature_text = models.CharField(max_length=200,
                                   help_text="Feature bullet point text")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        verbose_name = '3️⃣ Service Feature'
        verbose_name_plural = '3️⃣ Service Features (Bullet Points)'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.service.title} - {self.feature_text}"


class WhyChooseItem(models.Model):
    """Why Choose Us benefit items on services page"""
    title = models.CharField(max_length=100,
                            help_text="Benefit title (e.g., US-Based Expertise)")
    description = models.TextField(help_text="Benefit description")
    icon = models.CharField(max_length=100, default="verified",
                           help_text="Material icon name")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    is_active = models.BooleanField(default=True, help_text="Show on services page")
    
    class Meta:
        verbose_name = '4️⃣ Why Choose Item'
        verbose_name_plural = '4️⃣ Why Choose Items (Benefits)'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class WhyChooseImage(models.Model):
    """Image grid for Why Choose Us section on services page"""
    image = models.FileField(upload_to='services/why_choose/',
                         help_text="SVG image for Why Choose section")
    alt_text = models.CharField(max_length=200, help_text="Image alt text for SEO")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        verbose_name = '5️⃣ Why Choose Image'
        verbose_name_plural = '5️⃣ Why Choose Images (Image Grid)'
        ordering = ['order']
    
    def __str__(self):
        return f"Why Choose Image {self.order}"


class ServicesPageCTA(models.Model):
    """Lead capture CTA section on services page (singleton - only one record)"""
    heading = models.CharField(max_length=200,
                              default="Ready to Scale Your Business?")
    description = models.TextField(
        default="Get a free strategy call to explore solutions tailored to your needs")
    button_text = models.CharField(max_length=100, default="Send Inquiry")
    disclaimer_text = models.CharField(max_length=100,
                                      default="NO SPAM. ONLY SOLUTIONS.",
                                      help_text="Text below submit button")
    is_active = models.BooleanField(default=True,
                                   help_text="Show/hide entire CTA section")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '6️⃣ Services CTA'
        verbose_name_plural = '6️⃣ Services CTA Section'
    
    def __str__(self):
        return "Services Page CTA Section"


class CTAChecklist(models.Model):
    """Checklist items for services page CTA section"""
    cta_section = models.ForeignKey(ServicesPageCTA, on_delete=models.CASCADE,
                                   related_name='checklist_items')
    text = models.CharField(max_length=200,
                           help_text="Checklist item text")
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    is_active = models.BooleanField(default=True, help_text="Show this checklist item")
    
    class Meta:
        verbose_name = '7️⃣ CTA Checklist Item'
        verbose_name_plural = '7️⃣ CTA Checklist Items'
        ordering = ['order']
    
    def __str__(self):
        return self.text


# ==================== BLOG PAGE DYNAMIC CONTENT MODELS ====================

class BlogCategory(models.Model):
    """Blog post categories/tags"""
    name = models.CharField(max_length=100, unique=True,
                           help_text="Category name (e.g., Digital Marketing)")
    slug = models.SlugField(max_length=100, unique=True,
                           help_text="URL-friendly version (e.g., digital-marketing)")
    order = models.IntegerField(default=0, help_text="Display order in filter buttons")
    is_active = models.BooleanField(default=True, help_text="Show in category filters")
    
    class Meta:
        verbose_name = '1️⃣ Blog Category'
        verbose_name_plural = '1️⃣ Blog Categories'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Blog posts/articles"""
    title = models.CharField(max_length=200, help_text="Article title")
    slug = models.SlugField(max_length=200, unique=True,
                           help_text="URL slug (auto-generated from title)")
    excerpt = models.TextField(help_text="Short description (2-3 sentences)")
    content = models.TextField(help_text="Full article content (HTML supported)")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True,
                                      help_text="Article featured image")
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL,
                                null=True, related_name='posts',
                                help_text="Article category")
    author = models.CharField(max_length=100, default="Techlynx Team",
                             help_text="Author name")
    read_time = models.IntegerField(default=5,
                                   help_text="Estimated reading time in minutes")
    is_featured = models.BooleanField(default=False,
                                     help_text="Show as featured article on top")
    is_trending = models.BooleanField(default=False,
                                     help_text="Show in trending sidebar")
    trending_order = models.IntegerField(default=0,
                                        help_text="Order in trending list (1, 2, 3)")
    is_published = models.BooleanField(default=True,
                                      help_text="Published and visible on blog")
    published_date = models.DateField(help_text="Publication date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '2️⃣ Blog Post'
        verbose_name_plural = '2️⃣ Blog Posts'
        ordering = ['-published_date', '-created_at']
    
    def __str__(self):
        return self.title


# ==================== CAREERS PAGE DYNAMIC CONTENT MODELS ====================

class CareersHero(models.Model):
    """Careers page hero section (singleton)"""
    badge_text = models.CharField(max_length=100, default="Now Hiring: 12 Open Roles",
                                 help_text="Hero badge text")
    headline = models.TextField(default="Build the Future or Become the Face",
                               help_text="Main headline (HTML tags supported for styling)")
    subheadline = models.TextField(
        default="Join our elite team of developers and marketers driving global innovation, or receive world-class management for your talent brand.",
        help_text="Hero subtitle"
    )
    cta_primary_text = models.CharField(max_length=50, default="View Open Roles")
    cta_primary_url = models.CharField(max_length=200, default="#open-roles")
    cta_secondary_text = models.CharField(max_length=50, default="Get Represented")
    cta_secondary_url = models.CharField(max_length=200, default="#talent-services")
    hero_image = models.ImageField(upload_to='careers/', blank=True, null=True,
                                  help_text="Hero section image")
    testimonial_text = models.TextField(
        default="Working here felt like joining a family of geniuses.",
        help_text="Testimonial quote"
    )
    testimonial_author = models.CharField(max_length=100, 
                                         default="Sarah J., Senior Fullstack Engineer",
                                         help_text="Testimonial author name and title")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '1️⃣ Careers Hero'
        verbose_name_plural = '1️⃣ Careers Hero'
    
    def __str__(self):
        return "Careers Hero Section"


class CareersStat(models.Model):
    """Statistics displayed on careers page"""
    number = models.CharField(max_length=20, help_text="Stat number (e.g., 50+, 12M+)")
    label = models.CharField(max_length=100, help_text="Stat label/description")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '2️⃣ Career Stat'
        verbose_name_plural = '2️⃣ Career Stats'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.number} - {self.label}"


class JobDepartment(models.Model):
    """Job departments for filtering"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '3️⃣ Job Department'
        verbose_name_plural = '3️⃣ Job Departments'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class JobLocation(models.Model):
    """Job locations for filtering"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '4️⃣ Job Location'
        verbose_name_plural = '4️⃣ Job Locations'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class JobOpening(models.Model):
    """Job openings/positions"""
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    title = models.CharField(max_length=200, help_text="Job title")
    slug = models.SlugField(max_length=200, unique=True,
                           help_text="URL slug (auto-generated from title)")
    department = models.ForeignKey(JobDepartment, on_delete=models.SET_NULL,
                                  null=True, related_name='jobs')
    location = models.ForeignKey(JobLocation, on_delete=models.SET_NULL,
                                null=True, related_name='jobs')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES,
                               default='full-time')
    salary_range = models.CharField(max_length=100, blank=True,
                                   help_text="e.g., $140k - $180k or $70k + Commission")
    description = models.TextField(blank=True, help_text="Full job description")
    requirements = models.TextField(blank=True, help_text="Job requirements")
    application_url = models.URLField(blank=True, help_text="External application URL")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True, help_text="Show on careers page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '5️⃣ Job Opening'
        verbose_name_plural = '5️⃣ Job Openings'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title


class TalentManagement(models.Model):
    """Talent management section content (singleton)"""
    headline = models.CharField(max_length=200,
                               default="Scale Your Personal Brand Beyond Limits")
    description = models.TextField(
        default="We represent the next generation of culture-shapers. Our managers don't just find deals; they build legacies through strategic PR, legal protection, and blue-chip brand partnerships."
    )
    cta_text = models.CharField(max_length=50, default="Apply for Representation")
    cta_url = models.CharField(max_length=200, default="#application-form")
    image_1 = models.ImageField(upload_to='talent/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='talent/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='talent/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='talent/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '6️⃣ Talent Management'
        verbose_name_plural = '6️⃣ Talent Management'
    
    def __str__(self):
        return "Talent Management Section"


class TalentFeature(models.Model):
    """Features of talent management service"""
    icon = models.CharField(max_length=50, help_text="Material icon name (e.g., handshake)")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '7️⃣ Talent Feature'
        verbose_name_plural = '7️⃣ Talent Features'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class CareerApplication(models.Model):
    """Career/Talent application submissions"""
    APPLICATION_TYPE_CHOICES = [
        ('job', 'Joining the Tech/Marketing Team'),
        ('talent', 'Talent Representation'),
    ]
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES)
    job_position = models.ForeignKey(JobOpening, on_delete=models.SET_NULL, 
                                    null=True, blank=True,
                                    help_text="Applied job position (if applicable)")
    links = models.TextField(blank=True, help_text="Portfolio/Social media links")
    resume = models.FileField(upload_to='applications/', blank=True, null=True,
                             help_text="Resume or media kit")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '8️⃣ Career Application'
        verbose_name_plural = '8️⃣ Career Applications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.get_application_type_display()}"


# ==================== AI SOLUTIONS PAGE DYNAMIC CONTENT MODELS ====================

class AISolutionsHero(models.Model):
    """Hero section for AI Solutions page (singleton)"""
    badge_icon = models.CharField(max_length=100, default="psychology", 
                                  help_text="Material icon name")
    badge_text = models.CharField(max_length=100, default="Next-Gen AI Technology")
    headline = models.TextField(default="Transform Your Business with AI-Powered Intelligence")
    description = models.TextField(default="From intelligent chatbots to predictive analytics and machine learning models. We build custom AI solutions that automate workflows, enhance decision-making, and drive exponential growth.")
    cta_primary_text = models.CharField(max_length=100, default="Start AI Transformation")
    cta_primary_url = models.CharField(max_length=200, default="/contact")
    cta_secondary_text = models.CharField(max_length=100, default="View AI Case Studies")
    cta_secondary_url = models.CharField(max_length=200, default="/case-studies")
    
    # Hero metrics
    metric_title = models.CharField(max_length=100, default="AI Impact Forecast")
    metric_main = models.CharField(max_length=100, default="85% Cost Reduction")
    automation_rate = models.IntegerField(default=94, help_text="Percentage")
    time_saved = models.CharField(max_length=50, default="2,400h/mo")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 AI Hero Section'
        verbose_name_plural = '🤖 AI Hero Section'
    
    def __str__(self):
        return "AI Solutions Hero Section"


class AIService(models.Model):
    """Individual AI services offered"""
    icon = models.CharField(max_length=100, help_text="Material icon name (fallback)")
    icon_image = models.FileField(upload_to='services/ai_services/', blank=True, null=True,
                                   help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    feature_1 = models.CharField(max_length=200)
    feature_2 = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 AI Service'
        verbose_name_plural = '🤖 AI Services'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class AITechnology(models.Model):
    """AI Technologies/Frameworks used"""
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='services/ai_technologies/', 
                            help_text="SVG or PNG logo (preferably SVG)")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 AI Technology'
        verbose_name_plural = '🤖 AI Technologies'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class AITechnologyDetail(models.Model):
    """Detailed descriptions for technology stacks"""
    icon = models.CharField(max_length=100, help_text="Material icon name (fallback)")
    icon_image = models.FileField(upload_to='services/ai_tech_details/', blank=True, null=True,
                                   help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 AI Tech Detail'
        verbose_name_plural = '🤖 AI Tech Details'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class AIImplementationStep(models.Model):
    """Implementation process steps"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 Implementation Step'
        verbose_name_plural = '🤖 Implementation Steps'
        ordering = ['order']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class AIROIMetric(models.Model):
    """ROI metrics for AI solutions"""
    icon = models.CharField(max_length=100, help_text="Material icon name (fallback)")
    icon_image = models.FileField(upload_to='services/ai_roi_metrics/', blank=True, null=True,
                                   help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 ROI Metric'
        verbose_name_plural = '🤖 ROI Metrics'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class AIPerformanceMetric(models.Model):
    """Performance metrics with progress bars"""
    metric_name = models.CharField(max_length=100)
    percentage = models.IntegerField(help_text="Value between 0-100")
    color = models.CharField(max_length=50, default="green-400", 
                           help_text="Tailwind color class (e.g., green-400, blue-500)")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 Performance Metric'
        verbose_name_plural = '🤖 Performance Metrics'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.metric_name}: {self.percentage}%"


class AITestimonial(models.Model):
    """Testimonials specific to AI solutions"""
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200)
    client_photo = models.ImageField(upload_to='testimonials/ai/', blank=True, null=True)
    testimonial_text = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 AI Testimonial'
        verbose_name_plural = '🤖 AI Testimonials'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class AISolutionsCTA(models.Model):
    """Final CTA section (singleton)"""
    headline = models.TextField(default="Ready to Harness the Power of AI?")
    description = models.TextField(default="Join forward-thinking enterprises who are gaining competitive advantage through intelligent automation and AI-driven decision making.")
    cta_primary_text = models.CharField(max_length=100, default="Start Your AI Journey")
    cta_primary_url = models.CharField(max_length=200, default="/contact")
    cta_secondary_text = models.CharField(max_length=100, default="Schedule Demo")
    cta_secondary_url = models.CharField(max_length=200, default="/contact")
    footer_text = models.CharField(max_length=200, 
                                  default="Free AI readiness assessment included with every consultation.")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🤖 AI CTA Section'
        verbose_name_plural = '🤖 AI CTA Section'
    
    def __str__(self):
        return "AI Solutions CTA Section"


# ===========================================
# Web Development Page Models
# ===========================================

class WebDevHero(models.Model):
    """Hero section for Web Development page (singleton)"""
    badge_text = models.CharField(max_length=200, default="US-Based Enterprise Agency")
    headline = models.TextField(default="Scalable, <span class='text-primary'>SEO-First</span> Web Development")
    description = models.TextField(default="High-performance websites built with Next.js and WordPress to drive ROI. Get a future-proof digital presence that converts visitors into loyal customers.")
    cta_primary_text = models.CharField(max_length=100, default="Book a Free Consultation")
    cta_primary_url = models.CharField(max_length=200, default="/contact")
    cta_secondary_text = models.CharField(max_length=100, default="View Case Studies")
    cta_secondary_url = models.CharField(max_length=200, default="/case-studies")
    hero_image = models.ImageField(upload_to='services/web_dev/hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🌐 Web Dev Hero'
        verbose_name_plural = '🌐 Web Dev Hero'
    
    def __str__(self):
        return "Web Development Hero Section"


class WebDevService(models.Model):
    """Core service offerings"""
    icon = models.CharField(max_length=100, help_text="Material icon name (fallback)")
    icon_image = models.FileField(upload_to='services/web_dev/service_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    feature_1 = models.CharField(max_length=200)
    feature_2 = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🌐 Web Dev Service'
        verbose_name_plural = '🌐 Web Dev Services'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class WebDevStackFeature(models.Model):
    """Tech stack feature details"""
    icon = models.CharField(max_length=100, help_text="Material icon name (fallback)")
    icon_image = models.FileField(upload_to='services/web_dev/stack_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🌐 Stack Feature'
        verbose_name_plural = '🌐 Stack Features'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class WebDevTechnology(models.Model):
    """Technologies in the stack grid"""
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='services/web_dev/tech_logos/', help_text="SVG logo file")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🌐 Technology'
        verbose_name_plural = '🌐 Technologies'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class WebDevProcess(models.Model):
    """Development process steps"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🌐 Process Step'
        verbose_name_plural = '🌐 Process Steps'
        ordering = ['order']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class WebDevSEOBenefit(models.Model):
    """SEO benefits features"""
    icon = models.CharField(max_length=100, help_text="Material icon name (fallback)")
    icon_image = models.FileField(upload_to='services/web_dev/seo_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🌐 SEO Benefit'
        verbose_name_plural = '🌐 SEO Benefits'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class WebDevSEOMetric(models.Model):
    """SEO audit metrics"""
    metric_name = models.CharField(max_length=100)
    score = models.IntegerField(help_text="Score out of 100")
    color = models.CharField(max_length=50, default="green-400", help_text="Tailwind color class")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🌐 SEO Metric'
        verbose_name_plural = '🌐 SEO Metrics'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.metric_name}: {self.score}/100"


class WebDevCTA(models.Model):
    """Final CTA section (singleton)"""
    headline = models.TextField(default="Ready to Scale Your Online Presence?")
    description = models.TextField(default="Join dozens of US enterprises who have transformed their digital ROI with our SEO-first development approach.")
    cta_primary_text = models.CharField(max_length=100, default="Book Free Consultation")
    cta_primary_url = models.CharField(max_length=200, default="/contact")
    cta_secondary_text = models.CharField(max_length=100, default="Contact Sales")
    cta_secondary_url = models.CharField(max_length=200, default="/contact")
    footer_text = models.CharField(max_length=200, default="No credit card required. Initial consult is 100% free.")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '🌐 Web Dev CTA'
        verbose_name_plural = '🌐 Web Dev CTA'
    
    def __str__(self):
        return "Web Development CTA Section"

# ===========================================
# Digital Marketing Page Models
# ===========================================

class DigitalMarketingHero(models.Model):
    """Hero section for Digital Marketing page (singleton)"""
    badge_text = models.CharField(max_length=200, default="ROI-Focused Growth")
    badge_icon = models.CharField(max_length=100, default="trending_up")
    headline = models.TextField(default="Scale Your Business with <span class='text-primary'>Strategy-First</span> Marketing")
    description = models.TextField(default="High-performance, SEO-first digital growth services designed for measurable ROI. We help US-based brands dominate their niche through data-backed execution.")
    cta_primary_text = models.CharField(max_length=100, default="Start Your Growth Journey")
    cta_primary_url = models.CharField(max_length=200, default="/contact")
    cta_secondary_text = models.CharField(max_length=100, default="View Case Studies")
    cta_secondary_url = models.CharField(max_length=200, default="/case-studies")
    
    # Hero Stats
    growth_percentage = models.IntegerField(default=248, help_text="Revenue growth percentage")
    avg_cpc_reduction = models.DecimalField(max_digits=5, decimal_places=2, default=1.45)
    conversion_rate = models.DecimalField(max_digits=4, decimal_places=1, default=8.4)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '📈 Digital Marketing Hero'
        verbose_name_plural = '📈 Digital Marketing Hero'
    
    def __str__(self):
        return "Digital Marketing Hero Section"


class DigitalMarketingService(models.Model):
    """Marketing service offerings"""
    icon = models.CharField(max_length=100, help_text="Material icon name (fallback)")
    icon_image = models.FileField(upload_to='services/digital_marketing/service_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    feature_1 = models.CharField(max_length=200)
    feature_2 = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '📈 Marketing Service'
        verbose_name_plural = '📈 Marketing Services'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class DigitalMarketingStrategy(models.Model):
    """Strategy-first approach steps"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '📈 Strategy Step'
        verbose_name_plural = '📈 Strategy Steps'
        ordering = ['order']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class DigitalMarketingTestimonial(models.Model):
    """Client testimonials for digital marketing"""
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200, blank=True)
    client_photo = models.ImageField(upload_to='testimonials/digital_marketing/', blank=True, null=True)
    testimonial_text = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '📈 Marketing Testimonial'
        verbose_name_plural = '📈 Marketing Testimonials'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class DigitalMarketingMetric(models.Model):
    """Growth monitoring metrics"""
    title = models.CharField(max_length=200)
    growth_indicator = models.CharField(max_length=100, help_text="e.g., +12%, +$42k, 4.2x")
    chart_data = models.CharField(max_length=200, default="20,35,30,50,85", help_text="Comma-separated percentages for 5 bars")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '📈 Growth Metric'
        verbose_name_plural = '📈 Growth Metrics'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.title} ({self.growth_indicator})"
    
    def get_chart_data_list(self):
        """Convert chart_data string to list of integers"""
        return [int(x.strip()) for x in self.chart_data.split(',')]


class DigitalMarketingCTA(models.Model):
    """CTA section (singleton)"""
    icon = models.CharField(max_length=100, default="insights")
    headline = models.TextField(default="Ready to see these results for yourself?")
    description = models.TextField(default="Schedule a 15-minute strategy call and we'll show you exactly how we'd grow your specific brand.")
    cta_text = models.CharField(max_length=100, default="Book Your Free Strategy Call")
    cta_url = models.CharField(max_length=200, default="/contact")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '📈 Marketing CTA'
        verbose_name_plural = '📈 Marketing CTA'
    
    def __str__(self):
        return "Digital Marketing CTA Section"
    
    def has_add_permission(self, request):
        return not DigitalMarketingCTA.objects.exists()


# ============================================
# APP DEVELOPMENT PAGE MODELS
# ============================================

class AppDevHero(models.Model):
    """Hero section for App Development page"""
    badge_icon = models.CharField(max_length=50, default='phone_android')
    badge_text = models.CharField(max_length=100, default='Native & Cross-Platform Apps')
    headline = models.TextField()
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200)
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200)
    engagement_growth = models.IntegerField(default=320, help_text="User engagement growth percentage")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "App Dev Hero Section"
        verbose_name_plural = "App Dev Hero Sections"
        ordering = ['order']

    def __str__(self):
        return f"App Dev Hero - {self.headline[:50]}"


class AppDevService(models.Model):
    """App development services (iOS, Android, Cross-Platform, PWA)"""
    icon = models.CharField(max_length=50, default='phone_android')
    icon_image = models.FileField(upload_to='services/app_development/service_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    feature_1 = models.CharField(max_length=200)
    feature_2 = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "App Dev Service"
        verbose_name_plural = "App Dev Services"
        ordering = ['order']

    def __str__(self):
        return self.title


class AppDevStackFeature(models.Model):
    """Technology stack features"""
    icon = models.CharField(max_length=50, default='phone_android')
    icon_image = models.FileField(upload_to='services/app_development/stack_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "App Dev Stack Feature"
        verbose_name_plural = "App Dev Stack Features"
        ordering = ['order']

    def __str__(self):
        return self.title


class AppDevTechnology(models.Model):
    """Technology logos (Swift, Kotlin, React Native, Flutter, Firebase, GraphQL)"""
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='services/app_development/tech_logos/', blank=True, null=True, help_text="SVG logo file")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "App Dev Technology"
        verbose_name_plural = "App Dev Technologies"
        ordering = ['order']

    def __str__(self):
        return self.name


class AppDevProcess(models.Model):
    """Development process steps"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "App Dev Process Step"
        verbose_name_plural = "App Dev Process Steps"
        ordering = ['order']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class AppDevFeature(models.Model):
    """Enterprise features (Security, Notifications, Payment, Analytics)"""
    icon = models.CharField(max_length=50, default='security')
    icon_image = models.FileField(upload_to='services/app_development/feature_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "App Dev Feature"
        verbose_name_plural = "App Dev Features"
        ordering = ['order']

    def __str__(self):
        return self.title


class AppDevPerformanceMetric(models.Model):
    """Performance metrics for the dashboard"""
    title = models.CharField(max_length=200)
    value = models.CharField(max_length=50, help_text="e.g., '<2s', '99.8%', '68%', '4.7★'")
    percentage = models.IntegerField(help_text="Width percentage for progress bar (0-100)")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "App Dev Performance Metric"
        verbose_name_plural = "App Dev Performance Metrics"
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.value}"


class AppDevTestimonial(models.Model):
    """Client testimonials"""
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200)
    client_photo = models.ImageField(upload_to='testimonials/app_development/', blank=True, null=True)
    testimonial_text = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "App Dev Testimonial"
        verbose_name_plural = "App Dev Testimonials"
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class AppDevCTA(models.Model):
    """Final CTA section"""
    headline = models.TextField()
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200)
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200)
    footer_text = models.CharField(max_length=300, blank=True)
    footer_icon = models.CharField(max_length=50, default='verified_user')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "App Dev CTA Section"
        verbose_name_plural = "App Dev CTA Sections"

    def __str__(self):
        return f"App Dev CTA - {self.headline[:50]}"

    def save(self, *args, **kwargs):
        if not self.pk and AppDevCTA.objects.exists():
            return
        super().save(*args, **kwargs)

    @classmethod
    def can_add(cls):
        return not AppDevCTA.objects.exists()


# ==================== SEO AUDIT PAGE MODELS ====================

class SEOAuditHero(models.Model):
    """Hero section for SEO Audit page"""
    badge_icon = models.CharField(max_length=50, default='search')
    badge_text = models.CharField(max_length=100)
    headline = models.TextField()
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200, default='/contact/')
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200, default='/case-studies/')
    traffic_growth = models.IntegerField(help_text="Traffic growth percentage (e.g., 475)")
    domain_authority = models.IntegerField(help_text="Domain Authority number (e.g., 68)")
    keywords_ranked = models.IntegerField(help_text="Number of keywords ranked (e.g., 1247)")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "SEO Audit Hero"
        verbose_name_plural = "SEO Audit Hero"

    def __str__(self):
        return f"SEO Audit Hero - {self.traffic_growth}% Traffic Growth"

    def save(self, *args, **kwargs):
        if not self.pk and SEOAuditHero.objects.exists():
            return
        super().save(*args, **kwargs)


class SEOAuditService(models.Model):
    """SEO audit service offerings"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/seo_audit/service_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    feature_1 = models.CharField(max_length=200)
    feature_2 = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "SEO Audit Service"
        verbose_name_plural = "SEO Audit Services"
        ordering = ['order']

    def __str__(self):
        return self.title


class SEOAuditTool(models.Model):
    """Tools and technologies used"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/seo_audit/tool_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "SEO Audit Tool"
        verbose_name_plural = "SEO Audit Tools"
        ordering = ['order']

    def __str__(self):
        return self.title


class SEOAuditToolLogo(models.Model):
    """Tool/platform logos"""
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='services/seo_audit/tool_logos/', help_text="SVG logo file")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "SEO Tool Logo"
        verbose_name_plural = "SEO Tool Logos"
        ordering = ['order']

    def __str__(self):
        return self.name


class SEOAuditProcess(models.Model):
    """Audit process steps"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "SEO Audit Process"
        verbose_name_plural = "SEO Audit Process Steps"
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class SEOAuditResult(models.Model):
    """Results and benefits section"""
    headline = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "SEO Audit Result Section"
        verbose_name_plural = "SEO Audit Result Section"

    def __str__(self):
        return f"Results - {self.headline[:50]}"

    def save(self, *args, **kwargs):
        if not self.pk and SEOAuditResult.objects.exists():
            return
        super().save(*args, **kwargs)


class SEOAuditBenefit(models.Model):
    """Result benefits list"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/seo_audit/benefit_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "SEO Audit Benefit"
        verbose_name_plural = "SEO Audit Benefits"
        ordering = ['order']

    def __str__(self):
        return self.title


class SEOAuditHealthMetric(models.Model):
    """SEO health score metrics"""
    title = models.CharField(max_length=200)
    score = models.IntegerField(help_text="Score out of 100")
    percentage = models.IntegerField(help_text="Percentage for progress bar (0-100)")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "SEO Health Metric"
        verbose_name_plural = "SEO Health Metrics"
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.score}/100"


class SEOAuditTestimonial(models.Model):
    """Client testimonials"""
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200)
    client_photo = models.ImageField(upload_to='testimonials/seo_audit/', blank=True, null=True)
    testimonial_text = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "SEO Audit Testimonial"
        verbose_name_plural = "SEO Audit Testimonials"
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class SEOAuditCTA(models.Model):
    """Final CTA section"""
    headline = models.TextField()
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200)
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200)
    footer_text = models.CharField(max_length=300, blank=True)
    footer_icon = models.CharField(max_length=50, default='verified_user')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "SEO Audit CTA Section"
        verbose_name_plural = "SEO Audit CTA Sections"

    def __str__(self):
        return f"SEO Audit CTA - {self.headline[:50]}"

    def save(self, *args, **kwargs):
        if not self.pk and SEOAuditCTA.objects.exists():
            return
        super().save(*args, **kwargs)


# ==================== PROJECT MANAGEMENT PAGE MODELS ====================

class PMHero(models.Model):
    """Hero section for Project Management page"""
    badge_icon = models.CharField(max_length=50, default='task_alt')
    badge_text = models.CharField(max_length=100)
    headline = models.TextField()
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200, default='/contact/')
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200, default='/case-studies/')
    success_rate = models.DecimalField(max_digits=4, decimal_places=1, help_text="e.g., 98.5")
    ontime_delivery = models.IntegerField(help_text="Percentage (e.g., 95)")
    under_budget = models.IntegerField(help_text="Percentage (e.g., 18)")
    client_rating = models.DecimalField(max_digits=2, decimal_places=1, help_text="e.g., 4.9")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "PM Hero"
        verbose_name_plural = "PM Hero"

    def __str__(self):
        return f"PM Hero - {self.success_rate}% Success Rate"

    def save(self, *args, **kwargs):
        if not self.pk and PMHero.objects.exists():
            return
        super().save(*args, **kwargs)


class PMService(models.Model):
    """Project Management service offerings"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/project_management/service_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    feature_1 = models.CharField(max_length=200)
    feature_2 = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "PM Service"
        verbose_name_plural = "PM Services"
        ordering = ['order']

    def __str__(self):
        return self.title


class PMTool(models.Model):
    """PM tools and platforms"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/project_management/tool_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "PM Tool"
        verbose_name_plural = "PM Tools"
        ordering = ['order']

    def __str__(self):
        return self.title


class PMToolLogo(models.Model):
    """PM platform logos"""
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='services/project_management/tool_logos/', help_text="SVG logo file")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "PM Tool Logo"
        verbose_name_plural = "PM Tool Logos"
        ordering = ['order']

    def __str__(self):
        return self.name


class PMProcess(models.Model):
    """PM process steps"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "PM Process"
        verbose_name_plural = "PM Process Steps"
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class PMBenefit(models.Model):
    """PM benefits"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/project_management/benefit_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "PM Benefit"
        verbose_name_plural = "PM Benefits"
        ordering = ['order']

    def __str__(self):
        return self.title


class PMMetric(models.Model):
    """Project performance metrics"""
    title = models.CharField(max_length=200)
    value = models.CharField(max_length=50, help_text="e.g., 95%, 4.9/5.0")
    percentage = models.IntegerField(help_text="For progress bar (0-100)")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "PM Metric"
        verbose_name_plural = "PM Metrics"
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.value}"


class PMTestimonial(models.Model):
    """Client testimonials"""
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200)
    client_photo = models.ImageField(upload_to='testimonials/project_management/', blank=True, null=True)
    testimonial_text = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "PM Testimonial"
        verbose_name_plural = "PM Testimonials"
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class PMCTA(models.Model):
    """Final CTA section"""
    headline = models.TextField()
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200)
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200)
    footer_text = models.CharField(max_length=300, blank=True)
    footer_icon = models.CharField(max_length=50, default='verified_user')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "PM CTA Section"
        verbose_name_plural = "PM CTA Sections"

    def __str__(self):
        return f"PM CTA - {self.headline[:50]}"

    def save(self, *args, **kwargs):
        if not self.pk and PMCTA.objects.exists():
            return
        super().save(*args, **kwargs)


# ==================== VIRTUAL ASSISTANCE PAGE MODELS ====================

class VAHero(models.Model):
    """Hero section for Virtual Assistance page"""
    badge_icon = models.CharField(max_length=50, default='support_agent')
    badge_text = models.CharField(max_length=100)
    headline = models.TextField()
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200, default='/contact/')
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200, default='#services')
    hero_image = models.ImageField(upload_to='services/virtual_assistance/', blank=True, null=True)
    tasks_completed = models.IntegerField(help_text="Total tasks completed (e.g., 500)")
    support_availability = models.CharField(max_length=50, default='24/7')
    satisfaction_rate = models.IntegerField(help_text="Percentage (e.g., 98)")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "VA Hero"
        verbose_name_plural = "VA Hero"

    def __str__(self):
        return f"VA Hero - {self.tasks_completed} Tasks"

    def save(self, *args, **kwargs):
        if not self.pk and VAHero.objects.exists():
            return
        super().save(*args, **kwargs)


class VAService(models.Model):
    """Virtual Assistance service offerings"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/virtual_assistance/service_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    feature_1 = models.CharField(max_length=200)
    feature_2 = models.CharField(max_length=200)
    feature_3 = models.CharField(max_length=200)
    feature_4 = models.CharField(max_length=200)
    color_scheme = models.CharField(max_length=50, choices=[
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('orange', 'Orange'),
    ], default='purple')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "VA Service"
        verbose_name_plural = "VA Services"
        ordering = ['order']

    def __str__(self):
        return self.title


class VABenefit(models.Model):
    """Why Choose Us benefits"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/virtual_assistance/benefit_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    color_scheme = models.CharField(max_length=50, choices=[
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('orange', 'Orange'),
    ], default='purple')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "VA Benefit"
        verbose_name_plural = "VA Benefits"
        ordering = ['order']

    def __str__(self):
        return self.title


class VACTA(models.Model):
    """Call to Action section for Virtual Assistance page"""
    headline = models.CharField(max_length=200)
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200, default='/contact/')
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200, default='/case-studies/')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "VA CTA"
        verbose_name_plural = "VA CTA"

    def __str__(self):
        return f"VA CTA - {self.headline[:50]}"

    def save(self, *args, **kwargs):
        if not self.pk and VACTA.objects.exists():
            return
        super().save(*args, **kwargs)


# ==================== FINANCE & ACCOUNTING PAGE MODELS ====================

class FAHero(models.Model):
    """Hero section for Finance & Accounting page"""
    badge_icon = models.CharField(max_length=50, default='account_balance')
    badge_text = models.CharField(max_length=100)
    headline = models.TextField()
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200, default='/contact/')
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200, default='/case-studies/')
    hero_image = models.ImageField(upload_to='services/finance_accounting/', blank=True, null=True)
    cost_savings_percentage = models.IntegerField(help_text="Cost savings percentage (e.g., 42)")
    time_saved_monthly = models.IntegerField(help_text="Hours saved monthly (e.g., 280)")
    error_rate = models.FloatField(help_text="Error rate percentage (e.g., 0.02)")
    compliance_guarantee = models.CharField(max_length=100, default="100% Compliance Guarantee")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FA Hero"
        verbose_name_plural = "FA Hero"

    def __str__(self):
        return f"FA Hero - {self.cost_savings_percentage}% Savings"

    def save(self, *args, **kwargs):
        if not self.pk and FAHero.objects.exists():
            return
        super().save(*args, **kwargs)


class FAService(models.Model):
    """Finance & Accounting service offerings"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/finance_accounting/service_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    feature_1 = models.CharField(max_length=200)
    feature_2 = models.CharField(max_length=200)
    feature_3 = models.CharField(max_length=200, blank=True, null=True)
    feature_4 = models.CharField(max_length=200, blank=True, null=True)
    color_scheme = models.CharField(max_length=50, choices=[
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('orange', 'Orange'),
    ], default='blue')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "FA Service"
        verbose_name_plural = "FA Services"
        ordering = ['order']

    def __str__(self):
        return self.title


class FATool(models.Model):
    """Financial tools and software"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/finance_accounting/tool_icons/', blank=True, null=True, help_text="SVG icon file")
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, help_text="e.g., Cloud Accounting Platforms")
    description = models.TextField()
    color_scheme = models.CharField(max_length=50, choices=[
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('orange', 'Orange'),
    ], default='blue')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "FA Tool"
        verbose_name_plural = "FA Tools"
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.category}"


class FAProcess(models.Model):
    """Finance & Accounting process steps"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "FA Process"
        verbose_name_plural = "FA Process Steps"
        ordering = ['order']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class FABenefit(models.Model):
    """Finance & Accounting benefits"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/finance_accounting/benefit_icons/', blank=True, null=True, help_text="SVG icon file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    metric = models.CharField(max_length=100, help_text="e.g., 42% Cost Reduction")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "FA Benefit"
        verbose_name_plural = "FA Benefits"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.metric}"


class FATestimonial(models.Model):
    """Finance & Accounting testimonials"""
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=100)
    client_company = models.CharField(max_length=200)
    client_photo = models.ImageField(upload_to='testimonials/finance_accounting/', blank=True, null=True)
    testimonial_text = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "FA Testimonial"
        verbose_name_plural = "FA Testimonials"
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class FACTA(models.Model):
    """Call to Action section for Finance & Accounting page"""
    headline = models.CharField(max_length=200)
    description = models.TextField()
    cta_primary_text = models.CharField(max_length=100)
    cta_primary_url = models.CharField(max_length=200, default='/contact/')
    cta_secondary_text = models.CharField(max_length=100)
    cta_secondary_url = models.CharField(max_length=200, default='/contact/')
    guarantee_text = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FA CTA"
        verbose_name_plural = "FA CTA"

    def __str__(self):
        return f"FA CTA - {self.headline[:50]}"

    def save(self, *args, **kwargs):
        if not self.pk and FACTA.objects.exists():
            return
        super().save(*args, **kwargs)


# ============================================
# Content Production Models
# ============================================

class CPService(models.Model):
    """Content Production Services"""
    icon = models.CharField(max_length=50, help_text="Material icon name or SVG path")
    icon_image = models.FileField(upload_to='services/content_production/service_icons/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    features = models.JSONField(default=list, help_text="List of features")
    color_scheme = models.CharField(max_length=50, choices=[
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('orange', 'Orange'),
    ], default='blue')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "CP Service"
        verbose_name_plural = "CP Services"
        ordering = ['order']

    def __str__(self):
        return self.title


class CPTool(models.Model):
    """Content Production Tools"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/content_production/tool_icons/', blank=True, null=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, help_text="e.g., Design Suite, Video Editing")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "CP Tool"
        verbose_name_plural = "CP Tools"
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.category}"


class CPBenefit(models.Model):
    """Content Production Benefits/Results"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/content_production/benefit_icons/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    metric_value = models.CharField(max_length=50, help_text="e.g., 385%, 3.2x")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "CP Benefit"
        verbose_name_plural = "CP Benefits"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.metric_value}"


class CPProcessStep(models.Model):
    """Content Production Process Steps"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "CP Process Step"
        verbose_name_plural = "CP Process Steps"
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class CPMetric(models.Model):
    """Content Production Performance Metrics"""
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    percentage = models.IntegerField(help_text="Bar width percentage (0-100)")
    color_class = models.CharField(max_length=50, default='green-400')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "CP Metric"
        verbose_name_plural = "CP Metrics"
        ordering = ['order']

    def __str__(self):
        return f"{self.name}: {self.value}"


class CPTestimonial(models.Model):
    """Content Production Testimonials"""
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100)
    client_company = models.CharField(max_length=200)
    client_photo = models.URLField(blank=True)
    testimonial_text = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "CP Testimonial"
        verbose_name_plural = "CP Testimonials"
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class CPTechnology(models.Model):
    """Content Production Technology Categories"""
    icon = models.CharField(max_length=50, help_text="Material icon name")
    icon_image = models.FileField(upload_to='services/content_production/tech_icons/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "CP Technology"
        verbose_name_plural = "CP Technologies"
        ordering = ['order']

    def __str__(self):
        return self.title


# ==================== TESTIMONIALS PAGE MODELS ====================

class TestimonialsPageSEO(models.Model):
    """SEO settings for testimonials page (singleton)"""
    page_title = models.CharField(max_length=60, default="Client Testimonials | Real Results from Real Businesses")
    meta_description = models.TextField(max_length=160, 
        default="Read what our clients say about Techlynx Pro. Real testimonials from businesses we've helped grow with AI solutions, web development, and digital marketing.")
    meta_keywords = models.TextField(default="client testimonials, customer reviews, client success stories, business reviews, IT services reviews")
    og_title = models.CharField(max_length=60, default="Real Clients. Real Results. | Techlynx Pro")
    og_description = models.TextField(max_length=160, 
        default="Don't just take our word for it. See what businesses say about working with Techlynx Pro.")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Testimonials SEO"
        verbose_name_plural = "Testimonials SEO"
    
    def __str__(self):
        return "Testimonials Page SEO"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        if not self.pk and TestimonialsPageSEO.objects.exists():
            return TestimonialsPageSEO.objects.first()
        return super().save(*args, **kwargs)


class TestimonialsPageHero(models.Model):
    """Hero section for testimonials page (singleton)"""
    badge_icon = models.CharField(max_length=50, default="rate_review")
    badge_text = models.CharField(max_length=100, default="What Clients Say")
    headline = models.TextField(default="Real Clients. Real Results.")
    subheadline = models.CharField(max_length=200, default="(No Made-Up Quotes.)")
    description = models.TextField(
        default="We've been helping businesses grow online since 2015. Here's what clients say about working with Techlynx Pro—straight from the people who've actually worked with us.")
    cta_text = models.CharField(max_length=50, default="Get Quote")
    cta_url = models.CharField(max_length=200, default="/contact")
    cta_icon = models.CharField(max_length=50, default="arrow_forward")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Testimonials Hero"
        verbose_name_plural = "Testimonials Hero"
    
    def __str__(self):
        return "Testimonials Page Hero Section"
    
    def save(self, *args, **kwargs):
        if not self.pk and TestimonialsPageHero.objects.exists():
            return TestimonialsPageHero.objects.first()
        return super().save(*args, **kwargs)


class TestimonialsPageWhyChooseReason(models.Model):
    """Individual reasons for 'Why Choose' accordion"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_default_open = models.BooleanField(default=False, help_text="Open by default")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Why Choose Reason"
        verbose_name_plural = "Why Choose Reasons"
        ordering = ['order']
    
    def __str__(self):
        return self.title


class TestimonialsPageWhyChoose(models.Model):
    """Why Choose section for testimonials page (singleton)"""
    badge_icon = models.CharField(max_length=50, default="verified")
    badge_text = models.CharField(max_length=100, default="Why Choose Techlynx Pro")
    headline = models.CharField(max_length=200, default="Three Reasons Clients Stick With Us")
    description = models.TextField(
        default="We deliver experienced digital development services tailored to your business goals. With satisfied clients, we've proven our commitment to excellence.")
    illustration_image = models.ImageField(upload_to='testimonials/illustrated/', blank=True, null=True,
        help_text="Illustration image for the section")
    # Grid images for 2x2 layout
    grid_image_1 = models.ImageField(upload_to='services/why_choose/', blank=True, null=True,
        help_text="Top-left grid image")
    grid_image_2 = models.ImageField(upload_to='services/why_choose/', blank=True, null=True,
        help_text="Top-right grid image")
    grid_image_3 = models.ImageField(upload_to='services/why_choose/', blank=True, null=True,
        help_text="Bottom-left grid image")
    grid_image_4 = models.ImageField(upload_to='services/why_choose/', blank=True, null=True,
        help_text="Bottom-right grid image")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Why Choose Section"
        verbose_name_plural = "Why Choose Section"
    
    def __str__(self):
        return "Why Choose Section"
    
    def save(self, *args, **kwargs):
        if not self.pk and TestimonialsPageWhyChoose.objects.exists():
            return TestimonialsPageWhyChoose.objects.first()
        return super().save(*args, **kwargs)


class TestimonialsPageCTA(models.Model):
    """Final CTA section for testimonials page (singleton)"""
    badge_icon = models.CharField(max_length=50, default="phone")
    badge_text = models.CharField(max_length=50, default="Need Help?")
    headline = models.CharField(max_length=200, default="Ready to Get Started?")
    description = models.TextField(default="Join satisfied clients who trust Techlynx Pro for their digital needs.")
    cta_primary_text = models.CharField(max_length=50, default="Get Your Free Quote")
    cta_primary_url = models.CharField(max_length=200, default="/contact")
    cta_primary_icon = models.CharField(max_length=50, default="arrow_forward")
    cta_secondary_text = models.CharField(max_length=50, default="Call Us Now")
    cta_secondary_url = models.CharField(max_length=200, default="tel:+1234567890")
    cta_secondary_icon = models.CharField(max_length=50, default="phone")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Testimonials CTA"
        verbose_name_plural = "Testimonials CTA"
    
    def __str__(self):
        return "Testimonials Page CTA Section"
    
    def save(self, *args, **kwargs):
        if not self.pk and TestimonialsPageCTA.objects.exists():
            return TestimonialsPageCTA.objects.first()
        return super().save(*args, **kwargs)
