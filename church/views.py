# church/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import calendar
import json

from .models import (
    PrayerRequest, Testimony, ContactMessage, Donation, Event, 
    Ministry, Sermon, BibleVerse, Newsletter, ChurchSettings
)
from .forms import (
    PrayerRequestForm, TestimonyForm, ContactForm, DonationForm, 
    NewsletterForm, SearchForm
)


def get_church_settings():
    """Get church settings or create default if none exists"""
    try:
        return ChurchSettings.objects.first()
    except ChurchSettings.DoesNotExist:
        return ChurchSettings.objects.create()


def get_daily_verse():
    """Get today's Bible verse"""
    verses = BibleVerse.objects.filter(is_active=True)
    if verses.exists():
        # Use date to get consistent verse for the day
        today = timezone.now().date()
        verse_index = today.day % verses.count()
        return verses[verse_index]
    return None


def home(request):
    """Home page view"""
    context = {
        'church_settings': get_church_settings(),
        'daily_verse': get_daily_verse(),
        'upcoming_events': Event.objects.filter(date__gte=timezone.now().date()).order_by('date', 'start_time')[:3],
        'featured_testimonies': Testimony.objects.filter(status='approved', featured=True)[:3],
        'recent_sermons': Sermon.objects.filter(is_featured=True)[:3],
        'ministries': Ministry.objects.filter(is_active=True)[:6],
    }
    return render(request, 'church/home.html', context)


def about(request):
    """About page view"""
    context = {
        'church_settings': get_church_settings(),
        'ministries': Ministry.objects.filter(is_active=True),
    }
    return render(request, 'church/about.html', context)


def ministries(request):
    """Ministries page view"""
    context = {
        'church_settings': get_church_settings(),
        'ministries': Ministry.objects.filter(is_active=True),
    }
    return render(request, 'church/ministries.html', context)


def events(request):
    """Events and calendar page"""
    today = timezone.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Calendar data
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Get events for the month
    month_events = Event.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('date', 'start_time')
    
    # Create calendar with events
    calendar_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': '', 'events': []})
            else:
                day_events = month_events.filter(date__day=day)
                week_data.append({'day': day, 'events': list(day_events)})
        calendar_data.append(week_data)
    
    # Navigation dates
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    context = {
        'church_settings': get_church_settings(),
        'calendar_data': calendar_data,
        'month_name': month_name,
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'upcoming_events': Event.objects.filter(date__gte=today).order_by('date', 'start_time')[:5],
    }
    return render(request, 'church/events.html', context)


def prayer_request(request):
    """Prayer requests page"""
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            prayer_request = form.save()
            
            # Send email notification to church
            subject = f'New Prayer Request from {prayer_request.name}'
            message = f"""
            New prayer request received:
            
            Name: {prayer_request.name}
            Email: {prayer_request.email or 'Not provided'}
            Privacy: {prayer_request.get_privacy_display()}
            
            Request:
            {prayer_request.request_text}
            
            Submitted on: {prayer_request.created_at.strftime('%Y-%m-%d at %H:%M')}
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CHURCH_EMAIL, settings.PASTOR_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(
                request, 
                'Your prayer request has been submitted. Our prayer team will intercede for you.'
            )
            return redirect('prayer_request')
    else:
        form = PrayerRequestForm()
    
    context = {
        'church_settings': get_church_settings(),
        'form': form,
        'public_requests': PrayerRequest.objects.filter(
            privacy='public', 
            status='praying'
        ).order_by('-created_at')[:5],
    }
    return render(request, 'church/prayer_request.html', context)


def testimonies(request):
    """Testimonies page"""
    if request.method == 'POST':
        form = TestimonyForm(request.POST)
        if form.is_valid():
            testimony = form.save()
            
            # Send email notification to admin
            subject = f'New Testimony Submission: {testimony.title}'
            message = f"""
            New testimony submitted for review:
            
            Title: {testimony.title}
            Author: {testimony.name}
            
            Story:
            {testimony.story}
            
            Submitted on: {testimony.created_at.strftime('%Y-%m-%d at %H:%M')}
            
            Please review and approve/reject this testimony in the admin panel.
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CHURCH_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(
                request,
                'Thank you for sharing your testimony! It will be reviewed and published soon.'
            )
            return redirect('testimonies')
    else:
        form = TestimonyForm()
    
    # Get approved testimonies
    testimonies_list = Testimony.objects.filter(status='approved').order_by('-approved_at')
    
    # Pagination
    paginator = Paginator(testimonies_list, 6)
    page_number = request.GET.get('page')
    testimonies_page = paginator.get_page(page_number)
    
    context = {
        'church_settings': get_church_settings(),
        'form': form,
        'testimonies': testimonies_page,
        'featured_testimonies': Testimony.objects.filter(
            status='approved', 
            featured=True
        )[:3],
    }
    return render(request, 'church/testimonies.html', context)


def giving(request):
    """Donation/Giving page"""
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save()
            
            # Send confirmation email to donor
            donor_subject = 'Donation Confirmation - WOPBIC'
            donor_message = f"""
            Dear {donation.donor_name},
            
            Thank you for your generous donation to World of Prayer Bible International Church.
            
            Donation Details:
            Type: {donation.get_donation_type_display()}
            Amount: ₦{donation.amount:,.2f}
            Reference: {donation.transaction_reference}
            Date: {donation.created_at.strftime('%Y-%m-%d at %H:%M')}
            
            Your donation is currently being verified by our finance team. 
            You will receive another confirmation once the verification is complete.
            
            "God loves a cheerful giver" - 2 Corinthians 9:7
            
            God bless you!
            
            WOPBIC Finance Team
            """
            
            # Send notification to church finance team
            admin_subject = f'New Donation Submission - ₦{donation.amount:,.2f}'
            admin_message = f"""
            New donation submission received:
            
            Donor: {donation.donor_name}
            Email: {donation.donor_email}
            Phone: {donation.donor_phone or 'Not provided'}
            Type: {donation.get_donation_type_display()}
            Amount: ₦{donation.amount:,.2f}
            Reference: {donation.transaction_reference}
            
            Receipt uploaded: {'Yes' if donation.receipt_image else 'No'}
            
            Please verify this donation in the admin panel.
            """
            
            try:
                # Send to donor
                send_mail(
                    donor_subject,
                    donor_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [donation.donor_email],
                    fail_silently=True,
                )
                
                # Send to admin
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CHURCH_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(
                request,
                'Thank you for your donation! Your submission has been received and is being verified. '
                'You will receive a confirmation email shortly.'
            )
            return redirect('giving')
    else:
        form = DonationForm()
    
    context = {
        'church_settings': get_church_settings(),
        'form': form,
        'bank_details': settings.CHURCH_BANK_DETAILS,
        'recent_donations': Donation.objects.filter(
            status='verified'
        ).order_by('-verified_at')[:5],
    }
    return render(request, 'church/giving.html', context)


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send auto-reply to sender
            sender_subject = 'Thank you for contacting WOPBIC'
            sender_message = f"""
            Dear {contact_message.name},
            
            Thank you for reaching out to World of Prayer Bible International Church.
            We have received your message and will respond as soon as possible.
            
            Your Message:
            Subject: {contact_message.subject}
            {contact_message.message}
            
            If this is urgent, please call us at {get_church_settings().phone_primary}
            
            God bless you!
            
            WOPBIC Team
            """
            
            # Send notification to church
            admin_subject = f'New Contact Message: {contact_message.subject}'
            admin_message = f"""
            New contact message received:
            
            From: {contact_message.name}
            Email: {contact_message.email}
            Phone: {contact_message.phone or 'Not provided'}
            Subject: {contact_message.subject}
            
            Message:
            {contact_message.message}
            
            Received on: {contact_message.created_at.strftime('%Y-%m-%d at %H:%M')}
            """
            
            try:
                # Send auto-reply
                send_mail(
                    sender_subject,
                    sender_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_message.email],
                    fail_silently=True,
                )
                
                # Send to admin
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CHURCH_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(
                request,
                'Thank you for your message! We will get back to you soon.'
            )
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'church_settings': get_church_settings(),
        'form': form,
        'church_location': settings.CHURCH_LOCATION,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'church/contact.html', context)


def sermons(request):
    """Sermons page"""
    sermons_list = Sermon.objects.all().order_by('-date_preached')
    
    # Search functionality
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        sermons_list = sermons_list.filter(
            Q(title__icontains=query) |
            Q(preacher__icontains=query) |
            Q(scripture_reference__icontains=query) |
            Q(series__icontains=query)
        )
    
    # Filter by series
    series = request.GET.get('series')
    if series:
        sermons_list = sermons_list.filter(series=series)
    
    # Pagination
    paginator = Paginator(sermons_list, 9)
    page_number = request.GET.get('page')
    sermons_page = paginator.get_page(page_number)
    
    # Get available series for filter
    available_series = Sermon.objects.values_list('series', flat=True).distinct().exclude(series__isnull=True).exclude(series='')
    
    context = {
        'church_settings': get_church_settings(),
        'sermons': sermons_page,
        'search_form': search_form,
        'available_series': available_series,
        'featured_sermons': Sermon.objects.filter(is_featured=True)[:3],
    }
    return render(request, 'church/sermons.html', context)

def sermon_detail(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    
    # Increment download count if audio file is accessed
    if request.GET.get('download') and sermon.audio_file:
        sermon.download_count += 1
        sermon.save()
        return redirect(sermon.audio_file.url)
    
    # Convert YouTube URL to embed format
    video_embed_url = None
    if sermon.video_url:
        if 'youtube.com/watch?v=' in sermon.video_url:
            video_embed_url = sermon.video_url.replace('watch?v=', 'embed/')
        elif 'youtu.be/' in sermon.video_url:
            video_id = sermon.video_url.split('youtu.be/')[-1]
            video_embed_url = f'https://www.youtube.com/embed/{video_id}'
        else:
            video_embed_url = sermon.video_url
    
    # Get related sermons from same series
    related_sermons = Sermon.objects.filter(
        series=sermon.series
    ).exclude(pk=sermon.pk)[:3] if sermon.series else []
    
    context = {
        'church_settings': get_church_settings(),
        'sermon': sermon,
        'video_embed_url': video_embed_url,  # Add this
        'related_sermons': related_sermons,
    }
    return render(request, 'church/sermon_detail.html', context)


def newsletter_subscribe(request):
    """Newsletter subscription via AJAX"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if already subscribed
            if Newsletter.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'You are already subscribed to our newsletter.'
                })
            
            # Subscribe
            Newsletter.objects.create(email=email)
            
            # Send welcome email
            try:
                send_mail(
                    'Welcome to WOPBIC Newsletter',
                    f'''
                    Dear Subscriber,
                    
                    Thank you for subscribing to the World of Prayer Bible International Church newsletter!
                    
                    You will now receive updates about:
                    - Upcoming events and services
                    - New sermon releases
                    - Prayer requests and testimonies
                    - Church announcements
                    
                    God bless you!
                    
                    WOPBIC Team
                    ''',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Welcome email failed: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for subscribing to our newsletter!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def live_stream(request):
    """Live stream page"""
    context = {
        'church_settings': get_church_settings(),
        'next_service': Event.objects.filter(
            date__gte=timezone.now().date(),
            event_type='service'
        ).order_by('date', 'start_time').first(),
    }
    return render(request, 'church/live_stream.html', context)


def api_events(request):
    """API endpoint for calendar events (JSON)"""
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            events = Event.objects.filter(date__range=[start, end])
            events_data = []
            
            for event in events:
                events_data.append({
                    'id': event.id,
                    'title': event.title,
                    'start': f"{event.date}T{event.start_time}",
                    'end': f"{event.date}T{event.end_time}",
                    'description': event.description,
                    'type': event.event_type,
                    'location': event.location,
                })
            
            return JsonResponse(events_data, safe=False)
        except ValueError:
            pass
    
    return JsonResponse([], safe=False)


def search(request):
    """Global search functionality"""
    form = SearchForm(request.GET)
    results = {
        'sermons': [],
        'events': [],
        'testimonies': [],
        'query': ''
    }
    
    if form.is_valid():
        query = form.cleaned_data['query']
        results['query'] = query
        
        # Search sermons
        results['sermons'] = Sermon.objects.filter(
            Q(title__icontains=query) |
            Q(preacher__icontains=query) |
            Q(scripture_reference__icontains=query) |
            Q(summary__icontains=query)
        ).order_by('-date_preached')[:10]
        
        # Search events
        results['events'] = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        ).order_by('date')[:10]
        
        # Search testimonies
        results['testimonies'] = Testimony.objects.filter(
            Q(title__icontains=query) |
            Q(story__icontains=query),
            status='approved'
        ).order_by('-approved_at')[:10]
    
    context = {
        'church_settings': get_church_settings(),
        'form': form,
        'results': results,
    }
    return render(request, 'church/search.html', context)

def bible_verse_of_the_day(request):
    verse = BibleVerse.objects.filter(is_active=True).order_by('-created_at').first()
    return render(request, 'church/bible_verse.html', {'verse': verse})

