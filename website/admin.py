from django.contrib import admin
from .models import ContactInquiry, Newsletter

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
