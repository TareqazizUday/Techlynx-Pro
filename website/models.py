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
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.email}"


class Newsletter(models.Model):
    """Model to store newsletter subscriptions"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
