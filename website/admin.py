from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    ContactInquiry, Newsletter, HeroSection, HeroBenefit, CompanyStat,
    Service, Benefit, Guarantee, CaseStudy, CaseStudyMetric, CaseStudiesPageCTA, Testimonial,
    Partner, CTASection, ServicesPageHero, ServiceDetail, ServiceFeature,
    WhyChooseItem, WhyChooseImage, ServicesPageCTA, CTAChecklist,
    BlogCategory, BlogPost, CareersHero, CareersStat, JobDepartment,
    JobLocation, JobOpening, TalentManagement, TalentFeature, CareerApplication,
    AISolutionsHero, AIService, AITechnology, AITechnologyDetail,
    AIImplementationStep, AIROIMetric, AIPerformanceMetric, AITestimonial,
    AISolutionsCTA, WebDevHero, WebDevService, WebDevStackFeature,
    WebDevTechnology, WebDevProcess, WebDevSEOBenefit, WebDevSEOMetric, WebDevCTA,
    DigitalMarketingHero, DigitalMarketingService, DigitalMarketingStrategy,
    DigitalMarketingTestimonial, DigitalMarketingMetric, DigitalMarketingCTA,
    AppDevHero, AppDevService, AppDevStackFeature, AppDevTechnology,
    AppDevProcess, AppDevFeature, AppDevPerformanceMetric, AppDevTestimonial, AppDevCTA,
    SEOAuditHero, SEOAuditService, SEOAuditTool, SEOAuditToolLogo,
    SEOAuditProcess, SEOAuditResult, SEOAuditBenefit, SEOAuditHealthMetric,
    SEOAuditTestimonial, SEOAuditCTA,
    PMHero, PMService, PMTool, PMToolLogo, PMProcess, PMBenefit,
    PMMetric, PMTestimonial, PMCTA,
    VAHero, VAService, VABenefit, VACTA,
    FAHero, FAService, FATool, FAProcess, FABenefit, FATestimonial, FACTA,
    CPService, CPTool, CPBenefit, CPProcessStep, CPMetric, CPTestimonial, CPTechnology,
    TestimonialsPageSEO, TestimonialsPageHero, TestimonialsPageWhyChooseReason,
    TestimonialsPageWhyChoose, TestimonialsPageCTA
)



class TechlynxAdminSite(AdminSite):
    site_header = 'Techlynx Pro Administration'
    site_title = 'Techlynx Admin'
    index_title = 'Website Management Dashboard'
    
    def index(self, request, extra_context=None):
        """Override index to use custom template"""
        extra_context = extra_context or {}
        return super().index(request, extra_context)


# Use default admin site for now
admin.site.site_header = 'Techlynx Pro Administration'
admin.site.site_title = 'Techlynx Admin Portal'
admin.site.index_title = 'Website Management Dashboard'


# ==================== WEBSITE MANAGEMENT ====================

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'service_interest', 'created_at')
    list_filter = ('service_interest', 'created_at')
    search_fields = ('full_name', 'email', 'project_details')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    date_hierarchy = 'subscribed_at'
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscriber(s) activated.')
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscriber(s) deactivated.')
    deactivate_subscribers.short_description = "Deactivate selected subscribers"


# Helper function for admin image previews
def get_image_preview(image_field, size="100x60", fallback_text="No image"):
    """Safe image preview function for admin"""
    if image_field:
        try:
            return format_html(
                '<img src="{}" style="max-width: {}px; max-height: {}px; border-radius: 8px; object-fit: cover;">',
                image_field.url,
                size.split('x')[0],
                size.split('x')[1]
            )
        except:
            pass
    return mark_safe(f'<span style="color: #999;">{fallback_text}</span>')


# ==================== HOME PAGE CONTENT ADMIN ====================

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('headline', 'rating_score', 'image_preview', 'updated_at')
    readonly_fields = ('updated_at', 'image_preview')
    fieldsets = (
        ('Main Content', {
            'fields': ('headline', 'subheadline', 'rating_score', 'hero_image', 'image_preview')
        }),
        ('Call to Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        return get_image_preview(obj.hero_image if obj else None, "200x120", "No hero image")
    image_preview.short_description = 'Hero Image'
    
    def has_add_permission(self, request):
        return not HeroSection.objects.exists()


@admin.register(HeroBenefit)
class HeroBenefitAdmin(admin.ModelAdmin):
    list_display = ('value', 'title', 'icon', 'order')
    list_editable = ('order',)
    list_filter = ('title',)
    search_fields = ('title', 'value')
    ordering = ('order',)
    list_per_page = 10


@admin.register(CompanyStat)
class CompanyStatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('label', 'value')
    ordering = ('order',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    fieldsets = (
        ('Service Information', {
            'fields': ('title', 'description')
        }),
        ('Visual', {
            'fields': ('image', 'icon'),
            'description': 'Use image for professional look (preferred) or icon as fallback'
        }),
        ('Settings', {
            'fields': ('detail_page_url', 'is_active', 'order')
        }),
    )
    
    def image_preview(self, obj):
        if not obj or not obj.image:
            icon_text = f"Icon: {obj.icon}" if obj and obj.icon else "No image"
            return mark_safe(f'<span style="color: #999;">{icon_text}</span>')
        return get_image_preview(obj.image, "100x60")
    image_preview.short_description = 'Preview'


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    ordering = ('order',)


@admin.register(Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ('text', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('text',)
    ordering = ('order',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'photo_preview', 'rating', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'rating', 'created_at')
    search_fields = ('client_name', 'client_company', 'quote')
    readonly_fields = ('created_at', 'photo_preview')
    ordering = ('order',)
    
    fieldsets = (
        ('Client Info', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_photo', 'photo_preview')
        }),
        ('Testimonial', {
            'fields': ('quote', 'rating')
        }),
        ('Display', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def photo_preview(self, obj):
        if not obj or not obj.client_photo:
            return mark_safe('<span style="color: #999;">No photo</span>')
        return format_html(
            '<img src="{}" style="max-width: 50px; max-height: 50px; border-radius: 50%; object-fit: cover;">',
            obj.client_photo.url
        )
    photo_preview.short_description = 'Photo'


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'website_url', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    readonly_fields = ('logo_preview',)
    ordering = ('order',)
    
    fieldsets = (
        ('Partner Info', {
            'fields': ('name', 'logo', 'logo_preview', 'website_url')
        }),
        ('Display', {
            'fields': ('order',)
        }),
    )
    
    def logo_preview(self, obj):
        return get_image_preview(obj.logo if obj else None, "120x60", "No logo")
    logo_preview.short_description = 'Logo'


@admin.register(CTASection)
class CTASectionAdmin(admin.ModelAdmin):
    list_display = ('headline', 'updated_at')
    readonly_fields = ('updated_at',)
    
    def has_add_permission(self, request):
        return not CTASection.objects.exists()


# ==================== SERVICES PAGE CONTENT ADMIN ====================

@admin.register(ServicesPageHero)
class ServicesPageHeroAdmin(admin.ModelAdmin):
    list_display = ('headline', 'badge_text', 'image_preview', 'is_stat_visible', 'updated_at')
    readonly_fields = ('updated_at', 'image_preview')
    fieldsets = (
        ('Badge & Headline', {
            'fields': ('badge_text', 'headline', 'subheadline')
        }),
        ('Call to Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Hero Image', {
            'fields': ('hero_image', 'image_preview')
        }),
        ('Stat Badge', {
            'fields': ('stat_value', 'stat_label', 'stat_icon', 'is_stat_visible')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        return get_image_preview(obj.hero_image if obj else None, "200x120", "No hero image")
    image_preview.short_description = 'Hero Image'
    
    def has_add_permission(self, request):
        return not ServicesPageHero.objects.exists()


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 2
    fields = ('feature_text', 'order')
    ordering = ('order',)


@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    inlines = [ServiceFeatureInline]
    
    fieldsets = (
        ('Service Information', {
            'fields': ('title', 'description')
        }),
        ('Visual', {
            'fields': ('image', 'icon'),
            'description': 'Use image for professional look (preferred) or icon as fallback'
        }),
        ('Settings', {
            'fields': ('detail_page_url', 'order', 'is_active')
        }),
    )
    
    def image_preview(self, obj):
        if not obj or not obj.image:
            icon_text = f"Icon: {obj.icon}" if obj and obj.icon else "No image"
            return mark_safe(f'<span style="color: #999;">{icon_text}</span>')
        return get_image_preview(obj.image, "100x60")
    image_preview.short_description = 'Preview'


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ('service', 'feature_text', 'order')
    list_editable = ('order',)
    list_filter = ('service',)
    search_fields = ('feature_text', 'service__title')
    ordering = ('service', 'order')


@admin.register(WhyChooseItem)
class WhyChooseItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)


@admin.register(WhyChooseImage)
class WhyChooseImageAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image_preview', 'order')
    list_editable = ('order',)
    search_fields = ('alt_text',)
    readonly_fields = ('image_preview',)
    ordering = ('order',)
    
    fieldsets = (
        ('Image Info', {
            'fields': ('image', 'image_preview', 'alt_text')
        }),
        ('Display', {
            'fields': ('order',)
        }),
    )
    
    def image_preview(self, obj):
        return get_image_preview(obj.image if obj else None, "150x90", "No image")
    image_preview.short_description = 'Preview'


class CTAChecklistInline(admin.TabularInline):
    model = CTAChecklist
    extra = 1
    fields = ('text', 'order', 'is_active')
    ordering = ('order',)


@admin.register(ServicesPageCTA)
class ServicesPageCTAAdmin(admin.ModelAdmin):
    list_display = ('heading', 'is_active', 'updated_at')
    readonly_fields = ('updated_at',)
    list_editable = ('is_active',)
    inlines = [CTAChecklistInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('heading', 'description', 'button_text', 'disclaimer_text')
        }),
        ('Settings', {
            'fields': ('is_active', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        return not ServicesPageCTA.objects.exists()


@admin.register(CTAChecklist)
class CTAChecklistAdmin(admin.ModelAdmin):
    list_display = ('text', 'cta_section', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'cta_section')
    search_fields = ('text',)
    ordering = ('cta_section', 'order')


# ==================== BLOG PAGE CONTENT ADMIN ====================

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'category', 'author', 'published_date', 'is_published', 'is_featured', 'is_trending')
    list_editable = ('is_published', 'is_featured', 'is_trending')
    list_filter = ('is_published', 'is_featured', 'is_trending', 'category', 'published_date')
    search_fields = ('title', 'excerpt', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    ordering = ('-published_date', '-created_at')
    
    fieldsets = (
        ('Post Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image', 'image_preview')
        }),
        ('Metadata', {
            'fields': ('category', 'author', 'read_time', 'published_date')
        }),
        ('Visibility', {
            'fields': ('is_published', 'is_featured', 'is_trending', 'trending_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        return get_image_preview(obj.featured_image if obj else None, "120x80", "No featured image")
    image_preview.short_description = 'Featured Image'


# ==================== CASE STUDIES PAGE ====================

class CaseStudyMetricInline(admin.TabularInline):
    model = CaseStudyMetric
    extra = 1
    fields = ('label', 'value', 'order')


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'key_result_value', 'image_preview', 'is_active', 'is_featured', 'order', 'created_at')
    list_editable = ('is_active', 'is_featured', 'order')
    list_filter = ('is_active', 'is_featured', 'category', 'created_at')
    search_fields = ('title', 'description', 'category', 'client_name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'image_preview')
    ordering = ('order',)
    inlines = [CaseStudyMetricInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'client_name')
        }),
        ('Content', {
            'fields': ('description', 'detailed_description')
        }),
        ('Case Study Details', {
            'fields': ('challenge', 'solution', 'results'),
            'description': 'Detailed information for the case study detail page'
        }),
        ('Image', {
            'fields': ('background_image', 'image_alt_text', 'image_preview')
        }),
        ('Key Result', {
            'fields': ('key_result_label', 'key_result_value'),
            'description': 'Main result displayed on the card (e.g., "45% Ops Reduction")'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        return get_image_preview(obj.background_image if obj else None, "150x90", "No background image")
    image_preview.short_description = 'Background Image'


@admin.register(CaseStudiesPageCTA)
class CaseStudiesPageCTAAdmin(admin.ModelAdmin):
    list_display = ('headline', 'primary_button_text', 'secondary_button_text', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('CTA Content', {
            'fields': ('headline', 'description')
        }),
        ('Primary Button', {
            'fields': ('primary_button_text', 'primary_button_url')
        }),
        ('Secondary Button', {
            'fields': ('secondary_button_text', 'secondary_button_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one CTA
        return not CaseStudiesPageCTA.objects.exists()


# ==================== CAREERS PAGE CONTENT ADMIN ====================

@admin.register(CareersHero)
class CareersHeroAdmin(admin.ModelAdmin):
    list_display = ('headline', 'image_preview', 'is_active')
    readonly_fields = ('image_preview',)
    fieldsets = (
        ('Hero Content', {
            'fields': ('badge_text', 'headline', 'subheadline', 'hero_image', 'image_preview')
        }),
        ('Call to Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Testimonial', {
            'fields': ('testimonial_text', 'testimonial_author')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def image_preview(self, obj):
        return get_image_preview(obj.hero_image if obj else None, "200x120", "No hero image")
    image_preview.short_description = 'Hero Image'
    
    def has_add_permission(self, request):
        return not CareersHero.objects.exists()


@admin.register(CareersStat)
class CareersStatAdmin(admin.ModelAdmin):
    list_display = ('number', 'label', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('label', 'number')
    ordering = ('order',)


@admin.register(JobDepartment)
class JobDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(JobLocation)
class JobLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'job_type', 'salary_range', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'department', 'location', 'job_type', 'created_at')
    search_fields = ('title', 'description', 'requirements')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Job Details', {
            'fields': ('title', 'slug', 'department', 'location', 'job_type', 'salary_range')
        }),
        ('Description', {
            'fields': ('description', 'requirements')
        }),
        ('Application', {
            'fields': ('application_url',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TalentManagement)
class TalentManagementAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active')
    readonly_fields = ('image_1_preview', 'image_2_preview', 'image_3_preview', 'image_4_preview')
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'description', 'cta_text', 'cta_url')
        }),
        ('Gallery Images', {
            'fields': (
                ('image_1', 'image_1_preview'),
                ('image_2', 'image_2_preview'),
                ('image_3', 'image_3_preview'),
                ('image_4', 'image_4_preview')
            )
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def image_1_preview(self, obj):
        return get_image_preview(getattr(obj, 'image_1', None) if obj else None, "150x100", "No image")
    image_1_preview.short_description = 'Image 1'
    
    def image_2_preview(self, obj):
        return get_image_preview(getattr(obj, 'image_2', None) if obj else None, "150x100", "No image")
    image_2_preview.short_description = 'Image 2'
    
    def image_3_preview(self, obj):
        return get_image_preview(getattr(obj, 'image_3', None) if obj else None, "150x100", "No image")
    image_3_preview.short_description = 'Image 3'
    
    def image_4_preview(self, obj):
        return get_image_preview(getattr(obj, 'image_4', None) if obj else None, "150x100", "No image")
    image_4_preview.short_description = 'Image 4'
    
    def has_add_permission(self, request):
        return not TalentManagement.objects.exists()


@admin.register(TalentFeature)
class TalentFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)


@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'application_type', 'job_position', 'resume_link', 'created_at')
    list_filter = ('application_type', 'created_at', 'job_position')
    search_fields = ('full_name', 'email', 'links')
    readonly_fields = ('created_at', 'resume_link')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'application_type', 'job_position')
        }),
        ('Application Details', {
            'fields': ('links', 'resume', 'resume_link')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def resume_link(self, obj):
        if not obj or not obj.resume:
            return mark_safe('<span style="color: #999;">No resume uploaded</span>')
        try:
            return format_html(
                '<a href="{}" target="_blank" style="color: #0066cc; text-decoration: underline;">📄 View Resume</a>',
                obj.resume.url
            )
        except:
            return mark_safe('<span style="color: #999;">Resume file error</span>')
    resume_link.short_description = 'Resume'


# ==================== AI SOLUTIONS PAGE ====================

@admin.register(AISolutionsHero)
class AISolutionsHeroAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'automation_rate', 'is_active')
    fieldsets = (
        ('Badge & Headline', {
            'fields': ('badge_icon', 'badge_text', 'headline', 'description')
        }),
        ('Call-to-Actions', {
            'fields': (('cta_primary_text', 'cta_primary_url'), 
                      ('cta_secondary_text', 'cta_secondary_url'))
        }),
        ('Hero Metrics', {
            'fields': ('metric_title', 'metric_main', 'automation_rate', 'time_saved')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one hero section
        return not AISolutionsHero.objects.exists()


@admin.register(AIService)
class AIServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'icon', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
    fieldsets = (
        ('Service Information', {
            'fields': ('title', 'description')
        }),
        ('Icon', {
            'fields': ('icon_image', 'icon'),
            'description': 'Upload a custom icon image (PNG/SVG) or use material icon name as fallback'
        }),
        ('Features', {
            'fields': ('feature_1', 'feature_2')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 40px; object-fit: contain;" />', obj.icon_image.url)
        return format_html('<span class="material-symbols-outlined" style="color: #666;">{}=</span>', obj.icon)
    icon_preview.short_description = 'Icon'


@admin.register(AITechnology)
class AITechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 100px;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo Preview'


@admin.register(AITechnologyDetail)
class AITechnologyDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'icon', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
    fieldsets = (
        ('Technology Information', {
            'fields': ('title', 'description')
        }),
        ('Icon', {
            'fields': ('icon_image', 'icon'),
            'description': 'Upload a custom icon image (PNG/SVG) or use material icon name as fallback'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 40px; object-fit: contain;" />', obj.icon_image.url)
        return format_html('<span class="material-symbols-outlined" style="color: #666;">{}=</span>', obj.icon)
    icon_preview.short_description = 'Icon'


@admin.register(AIImplementationStep)
class AIImplementationStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(AIROIMetric)
class AIROIMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'icon', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
    fieldsets = (
        ('Metric Information', {
            'fields': ('title', 'description')
        }),
        ('Icon', {
            'fields': ('icon_image', 'icon'),
            'description': 'Upload a custom icon image (PNG/SVG) or use material icon name as fallback'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 40px; object-fit: contain;" />', obj.icon_image.url)
        return format_html('<span class="material-symbols-outlined" style="color: #666;">{}=</span>', obj.icon)
    icon_preview.short_description = 'Icon'


@admin.register(AIPerformanceMetric)
class AIPerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_name', 'percentage', 'color', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('metric_name',)
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(AITestimonial)
class AITestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'photo_preview', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('client_name', 'client_company', 'testimonial_text')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
    def photo_preview(self, obj):
        if obj.client_photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />', obj.client_photo.url)
        return '-'
    photo_preview.short_description = 'Photo'


@admin.register(AISolutionsCTA)
class AISolutionsCTAAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')
    fieldsets = (
        ('Headline & Description', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Actions', {
            'fields': (('cta_primary_text', 'cta_primary_url'),
                      ('cta_secondary_text', 'cta_secondary_url'))
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one CTA section
        return not AISolutionsCTA.objects.exists()


# ==================== WEB DEVELOPMENT PAGE ====================

@admin.register(WebDevHero)
class WebDevHeroAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')
    fieldsets = (
        ('Badge & Headline', {
            'fields': ('badge_text', 'headline', 'description')
        }),
        ('Call-to-Actions', {
            'fields': (('cta_primary_text', 'cta_primary_url'),
                      ('cta_secondary_text', 'cta_secondary_url'))
        }),
        ('Hero Image', {
            'fields': ('hero_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not WebDevHero.objects.exists()


@admin.register(WebDevService)
class WebDevServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    fieldsets = (
        ('Icon', {
            'fields': ('icon_image', 'icon')
        }),
        ('Content', {
            'fields': ('title', 'description', 'feature_1', 'feature_2')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: contain;" />', obj.icon_image.url)
        return format_html('<span class="material-symbols-outlined">{}</span>', obj.icon)
    icon_preview.short_description = 'Icon'


@admin.register(WebDevStackFeature)
class WebDevStackFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Icon', {
            'fields': ('icon_image', 'icon')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: contain;" />', obj.icon_image.url)
        return format_html('<span class="material-symbols-outlined">{}</span>', obj.icon)
    icon_preview.short_description = 'Icon'


@admin.register(WebDevTechnology)
class WebDevTechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: contain;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


@admin.register(WebDevProcess)
class WebDevProcessAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(WebDevSEOBenefit)
class WebDevSEOBenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Icon', {
            'fields': ('icon_image', 'icon')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: contain;" />', obj.icon_image.url)
        return format_html('<span class="material-symbols-outlined">{}</span>', obj.icon)
    icon_preview.short_description = 'Icon'


@admin.register(WebDevSEOMetric)
class WebDevSEOMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_name', 'score', 'color', 'order', 'is_active')
    list_editable = ('score', 'order', 'is_active')
    list_filter = ('is_active',)


@admin.register(WebDevCTA)
class WebDevCTAAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')
    fieldsets = (
        ('Headline & Description', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Actions', {
            'fields': (('cta_primary_text', 'cta_primary_url'),
                      ('cta_secondary_text', 'cta_secondary_url'))
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not WebDevCTA.objects.exists()


# ==================== DIGITAL MARKETING PAGE ====================

@admin.register(DigitalMarketingHero)
class DigitalMarketingHeroAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'growth_percentage', 'is_active')
    fieldsets = (
        ('Badge', {
            'fields': ('badge_text', 'badge_icon')
        }),
        ('Headline & Description', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Actions', {
            'fields': (('cta_primary_text', 'cta_primary_url'),
                      ('cta_secondary_text', 'cta_secondary_url'))
        }),
        ('Hero Stats', {
            'fields': ('growth_percentage', 'avg_cpc_reduction', 'conversion_rate')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not DigitalMarketingHero.objects.exists()


@admin.register(DigitalMarketingService)
class DigitalMarketingServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    fieldsets = (
        ('Icon', {
            'fields': ('icon_image', 'icon')
        }),
        ('Content', {
            'fields': ('title', 'description', 'feature_1', 'feature_2')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: contain;" />', obj.icon_image.url)
        return format_html('<span class="material-symbols-outlined">{}</span>', obj.icon)
    icon_preview.short_description = 'Icon'


@admin.register(DigitalMarketingStrategy)
class DigitalMarketingStrategyAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(DigitalMarketingTestimonial)
class DigitalMarketingTestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_position', 'client_company', 'photo_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('client_name', 'client_company', 'testimonial_text')
    
    def photo_preview(self, obj):
        if obj.client_photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />', obj.client_photo.url)
        return '-'
    photo_preview.short_description = 'Photo'


@admin.register(DigitalMarketingMetric)
class DigitalMarketingMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'growth_indicator', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    fieldsets = (
        ('Metric Info', {
            'fields': ('title', 'growth_indicator')
        }),
        ('Chart Data', {
            'fields': ('chart_data',),
            'description': 'Enter 5 comma-separated percentages (e.g., 20,35,30,50,85)'
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(DigitalMarketingCTA)
class DigitalMarketingCTAAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')
    fieldsets = (
        ('Icon & Headline', {
            'fields': ('icon', 'headline', 'description')
        }),
        ('Call-to-Action', {
            'fields': ('cta_text', 'cta_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not DigitalMarketingCTA.objects.exists()


# ============================================
# APP DEVELOPMENT PAGE ADMIN
# ============================================

@admin.register(AppDevHero)
class AppDevHeroAdmin(admin.ModelAdmin):
    list_display = ('headline', 'engagement_growth', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Badge', {
            'fields': ('badge_icon', 'badge_text')
        }),
        ('Content', {
            'fields': ('headline', 'description')
        }),
        ('Metrics', {
            'fields': ('engagement_growth',)
        }),
        ('Call-to-Action', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(AppDevService)
class AppDevServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Features', {
            'fields': ('feature_1', 'feature_2')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.icon_image.url)
        return '-'
    icon_preview.short_description = 'Icon Preview'


@admin.register(AppDevStackFeature)
class AppDevStackFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.icon_image.url)
        return '-'
    icon_preview.short_description = 'Icon Preview'


@admin.register(AppDevTechnology)
class AppDevTechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Technology', {
            'fields': ('name', 'logo')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="60" height="40" style="object-fit: contain;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo Preview'


@admin.register(AppDevProcess)
class AppDevProcessAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Process Step', {
            'fields': ('step_number', 'title', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(AppDevFeature)
class AppDevFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.icon_image.url)
        return '-'
    icon_preview.short_description = 'Icon Preview'


@admin.register(AppDevPerformanceMetric)
class AppDevPerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'percentage', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Metric', {
            'fields': ('title', 'value', 'percentage')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(AppDevTestimonial)
class AppDevTestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'photo_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Client Info', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_photo')
        }),
        ('Testimonial', {
            'fields': ('testimonial_text',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.client_photo:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 50%;" />', obj.client_photo.url)
        return '-'
    photo_preview.short_description = 'Photo Preview'


@admin.register(AppDevCTA)
class AppDevCTAAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Headline & Description', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Footer', {
            'fields': ('footer_icon', 'footer_text')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not AppDevCTA.objects.exists()


# ==================== SEO AUDIT PAGE ====================

@admin.register(SEOAuditHero)
class SEOAuditHeroAdmin(admin.ModelAdmin):
    list_display = ('traffic_growth', 'domain_authority', 'keywords_ranked', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Badge', {
            'fields': ('badge_icon', 'badge_text')
        }),
        ('Hero Content', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Stats', {
            'fields': ('traffic_growth', 'domain_authority', 'keywords_ranked')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not SEOAuditHero.objects.exists()


@admin.register(SEOAuditService)
class SEOAuditServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Service Details', {
            'fields': ('title', 'description', 'feature_1', 'feature_2')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.icon_image.url)
        return '-'
    icon_preview.short_description = 'Icon Preview'


@admin.register(SEOAuditTool)
class SEOAuditToolAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Tool Details', {
            'fields': ('title', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.icon_image.url)
        return '-'
    icon_preview.short_description = 'Icon Preview'


@admin.register(SEOAuditToolLogo)
class SEOAuditToolLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Logo', {
            'fields': ('name', 'logo')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="60" height="40" style="object-fit: contain;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo Preview'


@admin.register(SEOAuditProcess)
class SEOAuditProcessAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Step Details', {
            'fields': ('step_number', 'title', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(SEOAuditResult)
class SEOAuditResultAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Results Section', {
            'fields': ('headline', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not SEOAuditResult.objects.exists()


@admin.register(SEOAuditBenefit)
class SEOAuditBenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Benefit Details', {
            'fields': ('title', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.icon_image.url)
        return '-'
    icon_preview.short_description = 'Icon Preview'


@admin.register(SEOAuditHealthMetric)
class SEOAuditHealthMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'score', 'percentage', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Metric', {
            'fields': ('title', 'score', 'percentage')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(SEOAuditTestimonial)
class SEOAuditTestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'photo_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Client Info', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_photo')
        }),
        ('Testimonial', {
            'fields': ('testimonial_text',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.client_photo:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 50%;" />', obj.client_photo.url)
        return '-'
    photo_preview.short_description = 'Photo Preview'


@admin.register(SEOAuditCTA)
class SEOAuditCTAAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Headline & Description', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Footer', {
            'fields': ('footer_icon', 'footer_text')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not SEOAuditCTA.objects.exists()


# ==================== Project Management Page ====================

@admin.register(PMHero)
class PMHeroAdmin(admin.ModelAdmin):
    list_display = ('badge_text', 'success_rate', 'ontime_delivery', 'under_budget', 'client_rating', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('headline', 'description', 'badge_text')
    
    fieldsets = (
        ('Badge', {
            'fields': ('badge_icon', 'badge_text')
        }),
        ('Content', {
            'fields': ('headline', 'description')
        }),
        ('Metrics', {
            'fields': ('success_rate', 'ontime_delivery', 'under_budget', 'client_rating')
        }),
        ('Call-to-Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not PMHero.objects.exists()


@admin.register(PMService)
class PMServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'has_icon_image', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Features', {
            'fields': ('feature_1', 'feature_2')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def has_icon_image(self, obj):
        return bool(obj.icon_image)
    has_icon_image.boolean = True
    has_icon_image.short_description = 'Icon Image'


@admin.register(PMTool)
class PMToolAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'has_icon_image', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def has_icon_image(self, obj):
        return bool(obj.icon_image)
    has_icon_image.boolean = True
    has_icon_image.short_description = 'Icon Image'


@admin.register(PMToolLogo)
class PMToolLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 100px;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


@admin.register(PMProcess)
class PMProcessAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'description_preview', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('step_number',)
    
    fieldsets = (
        ('Step Information', {
            'fields': ('step_number', 'title', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Description'


@admin.register(PMBenefit)
class PMBenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'has_icon_image', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    fieldsets = (
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def has_icon_image(self, obj):
        return bool(obj.icon_image)
    has_icon_image.boolean = True
    has_icon_image.short_description = 'Icon Image'


@admin.register(PMMetric)
class PMMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'percentage', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'value')
    ordering = ('order',)
    
    fieldsets = (
        ('Metric Information', {
            'fields': ('title', 'value', 'percentage')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(PMTestimonial)
class PMTestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'client_position', 'has_photo', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('client_name', 'client_company', 'client_position')
    ordering = ('order',)
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_photo')
        }),
        ('Testimonial', {
            'fields': ('testimonial_text',)
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def has_photo(self, obj):
        return bool(obj.client_photo)
    has_photo.boolean = True
    has_photo.short_description = 'Photo'


@admin.register(PMCTA)
class PMCTAAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Footer', {
            'fields': ('footer_icon', 'footer_text')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not PMCTA.objects.exists()


# ==================== VIRTUAL ASSISTANCE PAGE MANAGEMENT ====================

@admin.register(VAHero)
class VAHeroAdmin(admin.ModelAdmin):
    list_display = ('tasks_completed', 'satisfaction_rate', 'is_active')
    fieldsets = (
        ('Badge', {
            'fields': ('badge_icon', 'badge_text')
        }),
        ('Content', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Action', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Hero Image', {
            'fields': ('hero_image',)
        }),
        ('Statistics', {
            'fields': ('tasks_completed', 'support_availability', 'satisfaction_rate')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not VAHero.objects.exists()


@admin.register(VAService)
class VAServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'color_scheme', 'order', 'is_active')
    list_filter = ('color_scheme', 'is_active')
    search_fields = ('title', 'description')
    ordering = ['order']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'order')
        }),
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Features', {
            'fields': ('feature_1', 'feature_2', 'feature_3', 'feature_4')
        }),
        ('Appearance', {
            'fields': ('color_scheme',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(VABenefit)
class VABenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'color_scheme', 'order', 'is_active')
    list_filter = ('color_scheme', 'is_active')
    search_fields = ('title', 'description')
    ordering = ['order']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'order')
        }),
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Appearance', {
            'fields': ('color_scheme',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(VACTA)
class VACTAAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active')
    
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not VACTA.objects.exists()


# ==================== FINANCE & ACCOUNTING PAGE ADMIN ====================

@admin.register(FAHero)
class FAHeroAdmin(admin.ModelAdmin):
    list_display = ('cost_savings_percentage', 'time_saved_monthly', 'error_rate', 'is_active')
    
    fieldsets = (
        ('Badge', {
            'fields': ('badge_icon', 'badge_text')
        }),
        ('Hero Content', {
            'fields': ('headline', 'description', 'hero_image')
        }),
        ('Call-to-Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Performance Metrics', {
            'fields': ('cost_savings_percentage', 'time_saved_monthly', 'error_rate', 'compliance_guarantee')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not FAHero.objects.exists()


@admin.register(FAService)
class FAServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'color_scheme', 'order', 'is_active')
    list_filter = ('color_scheme', 'is_active')
    search_fields = ('title', 'description')
    ordering = ['order']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'order')
        }),
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Features', {
            'fields': ('feature_1', 'feature_2', 'feature_3', 'feature_4')
        }),
        ('Appearance', {
            'fields': ('color_scheme',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(FATool)
class FAToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'color_scheme', 'order', 'is_active')
    list_filter = ('category', 'color_scheme', 'is_active')
    search_fields = ('name', 'category', 'description')
    ordering = ['order']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description', 'order')
        }),
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Appearance', {
            'fields': ('color_scheme',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(FAProcess)
class FAProcessAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ['order']
    
    fieldsets = (
        ('Process Step', {
            'fields': ('step_number', 'title', 'description', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(FABenefit)
class FABenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'metric', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'metric')
    ordering = ['order']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'metric', 'order')
        }),
        ('Icon', {
            'fields': ('icon', 'icon_image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(FATestimonial)
class FATestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('client_name', 'client_company', 'testimonial_text')
    ordering = ['order']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_photo')
        }),
        ('Testimonial', {
            'fields': ('testimonial_text',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(FACTA)
class FACTAAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active')
    
    fieldsets = (
        ('Content', {
            'fields': ('headline', 'description')
        }),
        ('Call-to-Action Buttons', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Guarantee', {
            'fields': ('guarantee_text',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not FACTA.objects.exists()


# ============================================
# Content Production Admin
# ============================================

@admin.register(CPService)
class CPServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'color_scheme')
    ordering = ('order',)


@admin.register(CPTool)
class CPToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'category', 'description')
    list_filter = ('is_active', 'category')
    ordering = ('order',)


@admin.register(CPBenefit)
class CPBenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'metric_value', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(CPProcessStep)
class CPProcessStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title', 'description')
    list_filter = ('is_active',)
    ordering = ('step_number',)


@admin.register(CPMetric)
class CPMetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'percentage', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(CPTestimonial)
class CPTestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('client_name', 'client_company', 'testimonial_text')
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(CPTechnology)
class CPTechnologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)


# ==================== TESTIMONIALS PAGE MANAGEMENT ====================

@admin.register(TestimonialsPageSEO)
class TestimonialsPageSEOAdmin(admin.ModelAdmin):
    list_display = ('page_title', 'updated_at')
    fieldsets = (
        ('Page Title & Description', {
            'fields': ('page_title', 'meta_description', 'meta_keywords')
        }),
        ('Open Graph (Social Media)', {
            'fields': ('og_title', 'og_description')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not TestimonialsPageSEO.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TestimonialsPageHero)
class TestimonialsPageHeroAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active', 'updated_at')
    fieldsets = (
        ('Badge', {
            'fields': ('badge_icon', 'badge_text')
        }),
        ('Headlines', {
            'fields': ('headline', 'subheadline', 'description')
        }),
        ('Call to Action', {
            'fields': ('cta_text', 'cta_url', 'cta_icon')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not TestimonialsPageHero.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TestimonialsPageWhyChooseReason)
class TestimonialsPageWhyChooseReasonAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_default_open', 'order', 'is_active')
    list_editable = ('is_default_open', 'order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'is_default_open')
    ordering = ('order',)


@admin.register(TestimonialsPageWhyChoose)
class TestimonialsPageWhyChooseAdmin(admin.ModelAdmin):
    list_display = ('headline', 'image_preview', 'is_active', 'updated_at')
    readonly_fields = ('image_preview', 'grid_preview_1', 'grid_preview_2', 'grid_preview_3', 'grid_preview_4')
    fieldsets = (
        ('Badge', {
            'fields': ('badge_icon', 'badge_text')
        }),
        ('Content', {
            'fields': ('headline', 'description')
        }),
        ('Illustration', {
            'fields': ('illustration_image', 'image_preview')
        }),
        ('Grid Images (2x2 Layout)', {
            'fields': (
                ('grid_image_1', 'grid_preview_1'),
                ('grid_image_2', 'grid_preview_2'),
                ('grid_image_3', 'grid_preview_3'),
                ('grid_image_4', 'grid_preview_4'),
            ),
            'description': 'Upload 4 images for the 2x2 grid layout in Why Choose section'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def image_preview(self, obj):
        return get_image_preview(obj.illustration_image if obj else None, "200x150", "No illustration image")
    image_preview.short_description = 'Image Preview'
    
    def grid_preview_1(self, obj):
        return get_image_preview(obj.grid_image_1 if obj else None, "150x150", "No image")
    grid_preview_1.short_description = 'Preview (Top-Left)'
    
    def grid_preview_2(self, obj):
        return get_image_preview(obj.grid_image_2 if obj else None, "150x150", "No image")
    grid_preview_2.short_description = 'Preview (Top-Right)'
    
    def grid_preview_3(self, obj):
        return get_image_preview(obj.grid_image_3 if obj else None, "150x150", "No image")
    grid_preview_3.short_description = 'Preview (Bottom-Left)'
    
    def grid_preview_4(self, obj):
        return get_image_preview(obj.grid_image_4 if obj else None, "150x150", "No image")
    grid_preview_4.short_description = 'Preview (Bottom-Right)'
    
    def has_add_permission(self, request):
        return not TestimonialsPageWhyChoose.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TestimonialsPageCTA)
class TestimonialsPageCTAAdmin(admin.ModelAdmin):
    list_display = ('headline', 'is_active', 'updated_at')
    fieldsets = (
        ('Badge', {
            'fields': ('badge_icon', 'badge_text')
        }),
        ('Content', {
            'fields': ('headline', 'description')
        }),
        ('Primary CTA', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_primary_icon')
        }),
        ('Secondary CTA', {
            'fields': ('cta_secondary_text', 'cta_secondary_url', 'cta_secondary_icon')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        return not TestimonialsPageCTA.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
