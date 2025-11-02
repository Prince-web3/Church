# church/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import EmailValidator
from PIL import Image


class PrayerRequest(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('praying', 'Being Prayed For'),
        ('answered', 'Answered'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True, validators=[EmailValidator()])
    request_text = models.TextField()
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='private')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prayer Request'
        verbose_name_plural = 'Prayer Requests'
    
    def __str__(self):
        return f"Prayer request from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class Testimony(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    story = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Testimony'
        verbose_name_plural = 'Testimonies'
    
    def __str__(self):
        return f"{self.title} by {self.name}"
    
    def approve(self):
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.save()
    
    def reject(self):
        self.status = 'rejected'
        self.save()


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200, default='General Inquiry')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class Donation(models.Model):
    DONATION_TYPES = [
        ('tithe', 'Tithes & Offerings'),
        ('building', 'Building Fund'),
        ('missions', 'Missions'),
        ('special', 'Special Offering'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField(validators=[EmailValidator()])
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
    
    def __str__(self):
        return f"₦{self.amount} donation from {self.donor_name} ({self.donation_type})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.receipt_image:
            img = Image.open(self.receipt_image.path)
            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.receipt_image.path)


class Event(models.Model):
    EVENT_TYPES = [
        ('service', 'Church Service'),
        ('prayer', 'Prayer Meeting'),
        ('bible_study', 'Bible Study'),
        ('youth', 'Youth Event'),
        ('conference', 'Conference'),
        ('outreach', 'Outreach'),
        ('special', 'Special Event'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, default='Main Sanctuary')
    is_recurring = models.BooleanField(default=False)
    recurring_pattern = models.CharField(max_length=50, blank=True, null=True)  # weekly, monthly, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    @property
    def is_past(self):
        return self.date < timezone.now().date()


class Ministry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    leader = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True, null=True)
    meeting_day = models.CharField(max_length=20, blank=True, null=True)
    meeting_time = models.TimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    icon_class = models.CharField(max_length=50, default='fas fa-cross')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Ministry'
        verbose_name_plural = 'Ministries'
    
    def __str__(self):
        return self.name


class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100, default='Pastor')
    scripture_reference = models.CharField(max_length=100)
    summary = models.TextField()
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    date_preached = models.DateField()
    series = models.CharField(max_length=100, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date_preached']
        verbose_name = 'Sermon'
        verbose_name_plural = 'Sermons'
    
    def __str__(self):
        return f"{self.title} - {self.date_preached}"


class BibleVerse(models.Model):
    verse_text = models.TextField()
    reference = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bible Verse'
        verbose_name_plural = 'Bible Verses'
    
    def __str__(self):
        return f"{self.reference}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
    
    def __str__(self):
        return self.email


class ChurchSettings(models.Model):
    site_name = models.CharField(max_length=200, default='World of Prayer Bible International Church')
    tagline = models.CharField(max_length=200, default='Fire Prayer City - Solution Ground')
    phone_primary = models.CharField(max_length=20, default='+234 800 123 4567')
    phone_secondary = models.CharField(max_length=20, blank=True, null=True)
    email_primary = models.EmailField(default='info@wopbic.org')
    email_prayer = models.EmailField(default='prayer@wopbic.org')
    address = models.TextField(default='123 Prayer Street, Fire City, Lagos State, Nigeria')
    facebook_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, default='2348001234567')
    sunday_service_time = models.TimeField(default='09:00')
    prayer_meeting_time = models.TimeField(default='18:00')
    youth_service_time = models.TimeField(default='18:00')
    
    class Meta:
        verbose_name = 'Church Settings'
        verbose_name_plural = 'Church Settings'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        if not self.pk and ChurchSettings.objects.exists():
            # Only allow one instance
            raise ValueError('Only one ChurchSettings instance is allowed.')
        super().save(*args, **kwargs)