# wopbic_project/urls.py (main project URLs)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('church.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Customize admin site
admin.site.site_header = "WOPBIC Administration"
admin.site.site_title = "WOPBIC Admin Portal"
admin.site.index_title = "Welcome to WOPBIC Administration"


# church/urls.py (app URLs)
from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('ministries/', views.ministries, name='ministries'),
    path('events/', views.events, name='events'),
    path('sermons/', views.sermons, name='sermons'),
    path('sermons/<int:pk>/', views.sermon_detail, name='sermon_detail'),
    path('giving/', views.giving, name='giving'),
    path('contact/', views.contact, name='contact'),
    
    # Interactive pages
    path('prayer/', views.prayer_request, name='prayer_request'),
    path('testimonies/', views.testimonies, name='testimonies'),
    path('live/', views.live_stream, name='live_stream'),
    path('search/', views.search, name='search'),
    path('verse-of-the-day/', views.bible_verse_of_the_day, name='verse_of_the_day'),
    
    # AJAX/API endpoints
    path('api/newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('api/events/', views.api_events, name='api_events'),
]