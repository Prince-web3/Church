# church/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    PrayerRequest, Testimony, ContactMessage, Donation, Event,
    Ministry, Sermon, BibleVerse, Newsletter, ChurchSettings
)


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'privacy', 'status', 'created_at')
    list_filter = ('privacy', 'status', 'created_at')
    search_fields = ('name', 'email', 'request_text')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Request Information', {
            'fields': ('name', 'email', 'privacy', 'request_text')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_praying', 'mark_as_answered']
    
    def mark_as_praying(self, request, queryset):
        updated = queryset.update(status='praying')
        self.message_user(request, f'{updated} prayer requests marked as being prayed for.')
    mark_as_praying.short_description = "Mark selected requests as being prayed for"
    
    def mark_as_answered(self, request, queryset):
        updated = queryset.update(status='answered')
        self.message_user(request, f'{updated} prayer requests marked as answered.')
    mark_as_answered.short_description = "Mark selected requests as answered"


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'status', 'featured', 'created_at', 'approved_at')
    list_filter = ('status', 'featured', 'created_at', 'approved_at')
    search_fields = ('title', 'name', 'story')
    readonly_fields = ('created_at', 'approved_at')
    list_per_page = 20
    
    fieldsets = (
        ('Testimony Information', {
            'fields': ('name', 'title', 'story')
        }),
        ('Status & Features', {
            'fields': ('status', 'featured', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'approved_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve_testimonies', 'reject_testimonies', 'feature_testimonies']
    
    def approve_testimonies(self, request, queryset):
        for testimony in queryset:
            if testimony.status != 'approved':
                testimony.approve()
                
                # Send approval email to testimony author (if we had their email)
                # For now, just count approvals
        
        count = queryset.filter(status='approved').count()
        self.message_user(request, f'{count} testimonies approved successfully.')
    approve_testimonies.short_description = "Approve selected testimonies"
    
    def reject_testimonies(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} testimonies rejected.')
    reject_testimonies.short_description = "Reject selected testimonies"
    
    def feature_testimonies(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} testimonies marked as featured.')
    feature_testimonies.short_description = "Feature selected testimonies"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_per_page = 20
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(status='read')
        self.message_user(request, f'{updated} messages marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} messages marked as replied.')
    mark_as_replied.short_description = "Mark selected messages as replied"


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'donation_type', 'status', 'created_at', 'receipt_link')
    list_filter = ('donation_type', 'status', 'created_at')
    search_fields = ('donor_name', 'donor_email', 'transaction_reference')
    readonly_fields = ('created_at', 'verified_at', 'receipt_preview')
    list_per_page = 20
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone')
        }),
        ('Donation Details', {
            'fields': ('donation_type', 'amount', 'transaction_reference')
        }),
        ('Receipt', {
            'fields': ('receipt_image', 'receipt_preview')
        }),
        ('Verification', {
            'fields': ('status', 'verified_at', 'admin_notes')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['verify_donations', 'reject_donations']
    
    def receipt_link(self, obj):
        if obj.receipt_image:
            return format_html('<a href="{}" target="_blank">View Receipt</a>', obj.receipt_image.url)
        return "No receipt"
    receipt_link.short_description = "Receipt"
    
    def receipt_preview(self, obj):
        if obj.receipt_image:
            return format_html('<img src="{}" style="max-width: 400px; max-height: 400px;" />', obj.receipt_image.url)
        return "No receipt uploaded"
    receipt_preview.short_description = "Receipt Preview"
    
    def verify_donations(self, request, queryset):
        from django.utils import timezone
        
        for donation in queryset:
            if donation.status != 'verified':
                donation.status = 'verified'
                donation.verified_at = timezone.now()
                donation.save()
                
                # Send verification email to donor
                try:
                    send_mail(
                        'Donation Verified - WOPBIC',
                        f'''
                        Dear {donation.donor_name},
                        
                        Your donation has been verified and received.
                        
                        Donation Details:
                        Type: {donation.get_donation_type_display()}
                        Amount: ₦{donation.amount:,.2f}
                        Reference: {donation.transaction_reference}
                        Verified on: {donation.verified_at.strftime('%Y-%m-%d')}
                        
                        Thank you for your generous support to the work of God's kingdom.
                        
                        May God bless you abundantly!
                        
                        WOPBIC Finance Team
                        ''',
                        settings.DEFAULT_FROM_EMAIL,
                        [donation.donor_email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Verification email failed: {e}")
        
        count = queryset.filter(status='verified').count()
        self.message_user(request, f'{count} donations verified successfully.')
    verify_donations.short_description = "Verify selected donations"
    
    def reject_donations(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} donations rejected.')
    reject_donations.short_description = "Reject selected donations"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'start_time', 'end_time', 'location', 'is_past')
    list_filter = ('event_type', 'date', 'is_recurring')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
    list_per_page = 20
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'event_type', 'location')
        }),
        ('Date & Time', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('Recurring', {
            'fields': ('is_recurring', 'recurring_pattern'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def is_past(self, obj):
        return obj.is_past
    is_past.boolean = True
    is_past.short_description = "Past Event"


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'meeting_day', 'meeting_time', 'is_active')
    list_filter = ('is_active', 'meeting_day')
    search_fields = ('name', 'leader', 'description')
    list_per_page = 20
    
    fieldsets = (
        ('Ministry Information', {
            'fields': ('name', 'description', 'leader', 'icon_class')
        }),
        ('Contact', {
            'fields': ('contact_email',)
        }),
        ('Meeting Schedule', {
            'fields': ('meeting_day', 'meeting_time')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'scripture_reference', 'date_preached', 'is_featured', 'download_count')
    list_filter = ('is_featured', 'date_preached', 'series')
    search_fields = ('title', 'preacher', 'scripture_reference', 'summary')
    readonly_fields = ('download_count',)
    date_hierarchy = 'date_preached'
    list_per_page = 20
    
    fieldsets = (
        ('Sermon Information', {
            'fields': ('title', 'preacher', 'scripture_reference', 'summary', 'series')
        }),
        ('Media', {
            'fields': ('audio_file', 'video_url')
        }),
        ('Details', {
            'fields': ('date_preached', 'is_featured', 'download_count')
        })
    )
    
    actions = ['feature_sermons']
    
    def feature_sermons(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} sermons marked as featured.')
    feature_sermons.short_description = "Feature selected sermons"

@admin.register(BibleVerse)
class BibleVerseAdmin(admin.ModelAdmin):
    list_display = ('reference', 'verse_preview', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('reference', 'verse_text')
    list_per_page = 20

    readonly_fields = ('created_at',)  # ✅ add this line

    fieldsets = (
        ('Verse Information', {
            'fields': ('verse_text', 'reference', 'is_active')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def verse_preview(self, obj):
        return obj.verse_text[:50] + '...' if len(obj.verse_text) > 50 else obj.verse_text
    verse_preview.short_description = "Verse Preview"



@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    list_per_page = 50
    
    actions = ['export_emails', 'deactivate_subscriptions']
    
    def export_emails(self, request, queryset):
        emails = queryset.filter(is_active=True).values_list('email', flat=True)
        email_list = ', '.join(emails)
        self.message_user(request, f'Active emails: {email_list}')
    export_emails.short_description = "Export selected email addresses"
    
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscriptions deactivated.')
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"


@admin.register(ChurchSettings)
class ChurchSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'tagline')
        }),
        ('Contact Information', {
            'fields': ('phone_primary', 'phone_secondary', 'email_primary', 'email_prayer', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'youtube_url', 'instagram_url', 'twitter_url', 'whatsapp_number')
        }),
        ('Service Times', {
            'fields': ('sunday_service_time', 'prayer_meeting_time', 'youth_service_time')
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not ChurchSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False