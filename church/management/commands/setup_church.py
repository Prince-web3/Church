# church/management/commands/setup_church.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from church.models import (
    ChurchSettings, BibleVerse, Ministry, Event
)
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Initial setup for church website'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting church setup...'))
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating admin user...')
            User.objects.create_superuser(
                username='admin',
                email='admin@wopbic.org',
                password='admin123'  # Change this!
            )
            self.stdout.write(self.style.SUCCESS('Admin user created (username: admin, password: admin123)'))
            self.stdout.write(self.style.WARNING('PLEASE CHANGE THE ADMIN PASSWORD IMMEDIATELY!'))
        
        # Create Church Settings
        if not ChurchSettings.objects.exists():
            self.stdout.write('Creating church settings...')
            ChurchSettings.objects.create(
                site_name='World of Prayer Bible International Church',
                tagline='Fire Prayer City - Solution Ground',
                phone_primary='+234 800 123 4567',
                phone_secondary='+234 801 234 5678',
                email_primary='info@wopbic.org',
                email_prayer='prayer@wopbic.org',
                address='123 Prayer Street, Fire City, Lagos State, Nigeria',
                whatsapp_number='2348001234567',
            )
            self.stdout.write(self.style.SUCCESS('Church settings created'))
        
        # Create Bible Verses
        if BibleVerse.objects.count() == 0:
            self.stdout.write('Adding Bible verses...')
            verses = [
                {
                    'verse_text': 'For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, to give you hope and a future.',
                    'reference': 'Jeremiah 29:11'
                },
                {
                    'verse_text': 'Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.',
                    'reference': 'Proverbs 3:5-6'
                },
                {
                    'verse_text': 'The Lord your God is with you, the Mighty Warrior who saves. He will take great delight in you; in his love he will no longer rebuke you, but will rejoice over you with singing.',
                    'reference': 'Zephaniah 3:17'
                },
                {
                    'verse_text': 'And we know that in all things God works for the good of those who love him, who have been called according to his purpose.',
                    'reference': 'Romans 8:28'
                },
                {
                    'verse_text': 'Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.',
                    'reference': 'Joshua 1:9'
                },
                {
                    'verse_text': 'The Lord is my shepherd, I lack nothing. He makes me lie down in green pastures, he leads me beside quiet waters, he refreshes my soul.',
                    'reference': 'Psalm 23:1-3'
                },
                {
                    'verse_text': 'Cast all your anxiety on him because he cares for you.',
                    'reference': '1 Peter 5:7'
                },
            ]
            
            for verse_data in verses:
                BibleVerse.objects.create(**verse_data)
            
            self.stdout.write(self.style.SUCCESS(f'{len(verses)} Bible verses added'))
        
        # Create Ministries
        if Ministry.objects.count() == 0:
            self.stdout.write('Creating ministries...')
            ministries = [
                {
                    'name': "Children's Ministry",
                    'description': 'Building strong spiritual foundations in young hearts through age-appropriate teaching and activities.',
                    'leader': 'Sister Grace',
                    'icon_class': 'fas fa-child',
                    'meeting_day': 'Sunday',
                },
                {
                    'name': 'Youth Ministry',
                    'description': 'Empowering the next generation for Christ through dynamic worship, relevant teaching, and fellowship.',
                    'leader': 'Brother David',
                    'icon_class': 'fas fa-users',
                    'meeting_day': 'Friday',
                },
                {
                    'name': "Men's Ministry",
                    'description': 'Raising godly men and fathers who will be spiritual leaders in their homes and communities.',
                    'leader': 'Elder John',
                    'icon_class': 'fas fa-male',
                    'meeting_day': 'Saturday',
                },
                {
                    'name': "Women's Ministry",
                    'description': 'Empowering women to fulfill their divine calling through prayer, fellowship, and service.',
                    'leader': 'Sister Mary',
                    'icon_class': 'fas fa-female',
                    'meeting_day': 'Thursday',
                },
                {
                    'name': 'Evangelism & Outreach',
                    'description': 'Reaching the world with the Gospel through local outreach and global missions.',
                    'leader': 'Pastor Michael',
                    'icon_class': 'fas fa-globe-africa',
                    'meeting_day': 'Saturday',
                },
                {
                    'name': 'Prayer Ministry',
                    'description': 'Interceding for our community, nation, and world through fervent prayer.',
                    'leader': 'Deaconess Faith',
                    'icon_class': 'fas fa-praying-hands',
                    'meeting_day': 'Wednesday',
                },
            ]
            
            for ministry_data in ministries:
                Ministry.objects.create(**ministry_data)
            
            self.stdout.write(self.style.SUCCESS(f'{len(ministries)} ministries created'))
        
        # Create sample events
        if Event.objects.count() == 0:
            self.stdout.write('Creating sample events...')
            today = datetime.now().date()
            
            # Regular weekly events
            events = [
                {
                    'title': 'Sunday Service',
                    'description': 'Join us for worship, prayer, and the Word of God.',
                    'event_type': 'service',
                    'date': today + timedelta(days=(6 - today.weekday())),  # Next Sunday
                    'start_time': '09:00',
                    'end_time': '12:00',
                    'location': 'Main Sanctuary',
                    'is_recurring': True,
                    'recurring_pattern': 'weekly',
                },
                {
                    'title': 'Prayer Meeting',
                    'description': 'Come and intercede with us for our community and nation.',
                    'event_type': 'prayer',
                    'date': today + timedelta(days=(2 - today.weekday()) % 7),  # Next Wednesday
                    'start_time': '18:00',
                    'end_time': '20:00',
                    'location': 'Prayer Hall',
                    'is_recurring': True,
                    'recurring_pattern': 'weekly',
                },
                {
                    'title': 'Youth Night',
                    'description': 'Dynamic worship, teaching, and fellowship for young people.',
                    'event_type': 'youth',
                    'date': today + timedelta(days=(4 - today.weekday()) % 7),  # Next Friday
                    'start_time': '18:00',
                    'end_time': '21:00',
                    'location': 'Youth Center',
                    'is_recurring': True,
                    'recurring_pattern': 'weekly',
                },
            ]
            
            for event_data in events:
                Event.objects.create(**event_data)
            
            self.stdout.write(self.style.SUCCESS(f'{len(events)} events created'))
        
        self.stdout.write(self.style.SUCCESS('\n================================='))
        self.stdout.write(self.style.SUCCESS('Church setup completed!'))
        self.stdout.write(self.style.SUCCESS('================================='))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Run: python manage.py runserver')
        self.stdout.write('2. Visit: http://localhost:8000/admin/')
        self.stdout.write('3. Login with: admin / admin123')
        self.stdout.write('4. CHANGE THE ADMIN PASSWORD!')
        self.stdout.write('5. Update church settings in admin panel')
        self.stdout.write('\n')