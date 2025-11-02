# WOPBIC Church Website - Django Backend Setup

Complete Django backend for World of Prayer Bible International Church website with all requested features.

## Features Implemented

✅ **Prayer Requests** - Sent to your email automatically  
✅ **Testimonies** - Submitted for review, you approve/decline via admin panel  
✅ **Donations** - Shows bank account details (Ecobank), users upload receipt  
✅ **Contact Form** - Messages sent to your email  
✅ **Google Maps Integration** - Shows church location  
✅ **Events Calendar** - Manage church events  
✅ **Sermons** - Upload audio/video sermons  
✅ **Newsletter Subscription**  
✅ **Admin Panel** - Full control over all content  

**Removed**: Member registration and login (as requested)

## Project Structure

```
wopbic_project/
├── wopbic_project/
│   ├── __init__.py
│   ├── settings.py          # Main settings
│   ├── urls.py              # Main URL config
│   └── wsgi.py
├── church/                   # Main app
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── setup_church.py
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form definitions
│   └── urls.py              # App URLs
├── templates/
│   └── church/
│       ├── base.html
│       ├── home.html
│       ├── about.html
│       ├── ministries.html
│       ├── events.html
│       ├── sermons.html
│       ├── giving.html
│       ├── prayer_request.html
│       ├── testimonies.html
│       ├── contact.html
│       └── live_stream.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│       ├── wopbic.jpg       # Church logo
│       ├── wopbic1.jpg      # Hero image
│       └── wopbic3.jpeg     # About image
├── media/
│   ├── receipts/            # Donation receipts
│   └── sermons/
├── .env                      # Environment variables (create this)
├── .env.example             # Template for .env
├── requirements.txt
├── manage.py
└── README.md
```

## Installation Steps

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool

### 2. Clone or Download Project Files

```bash
# Create project directory
mkdir wopbic_website
cd wopbic_website
```

### 3. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your actual values
# Use a text editor to update:
# - SECRET_KEY (generate a new one for security)
# - EMAIL settings (Gmail example provided)
# - CHURCH_EMAIL and PASTOR_EMAIL
# - GOOGLE_MAPS_API_KEY (optional but recommended)
```

#### Email Configuration (Gmail Example)

1. Go to your Gmail account
2. Enable 2-Factor Authentication
3. Generate an App Password: https://myaccount.google.com/apppasswords
4. Use the app password in `.env`:

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
```

### 6. Set Up Database

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Run initial setup (creates admin user, sample data)
python manage.py setup_church
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`
- **⚠️ CHANGE THIS IMMEDIATELY AFTER FIRST LOGIN!**

### 7. Copy Your Images

Copy your church images to the `static/images/` directory:
- `wopbic.jpg` - Church logo
- `wopbic1.jpg` - Homepage hero background
- `wopbic3.jpeg` - About section image

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000/

## Admin Panel Access

URL: http://localhost:8000/admin/

### What You Can Do in Admin:

1. **Prayer Requests** - View all requests, mark as "praying" or "answered"
2. **Testimonies** - Review and approve/reject submissions
3. **Donations** - Verify donations, view receipts
4. **Contact Messages** - Read and respond to messages
5. **Events** - Add/edit church events
6. **Sermons** - Upload sermons with audio/video
7. **Ministries** - Manage ministry information
8. **Bible Verses** - Add verses for daily display
9. **Church Settings** - Update contact info, service times, social media
10. **Newsletter** - View email subscribers

## Bank Account Configuration

The bank details are configured in `settings.py`:

```python
CHURCH_BANK_DETAILS = {
    'BANK_NAME': 'Ecobank Nigeria',
    'ACCOUNT_NAME': 'World of Prayer Bible International Church',
    'ACCOUNT_NUMBER': '1234567890',  # UPDATE THIS
    'SORT_CODE': '050150',  # UPDATE THIS
}
```

**⚠️ Update these with your actual bank details!**

## Google Maps Setup

1. Get a Google Maps API key: https://developers.google.com/maps/documentation/javascript/get-api-key
2. Add it to `.env`:
```
GOOGLE_MAPS_API_KEY=your-api-key-here
```
3. Update church coordinates in `.env`:
```
CHURCH_LATITUDE=6.5244
CHURCH_LONGITUDE=3.3792
```

## Email Notifications

The system sends emails for:

1. **Prayer Requests** → Sent to CHURCH_EMAIL and PASTOR_EMAIL
2. **Testimonies** → Sent to CHURCH_EMAIL for review
3. **Donations** → Confirmation to donor, notification to CHURCH_EMAIL
4. **Contact Messages** → Auto-reply to sender, notification to CHURCH_EMAIL

## How It Works

### Prayer Requests
1. User fills form on website
2. Request saved to database
3. Email sent to your church email
4. You review in admin panel
5. Mark as "praying" or "answered"

### Testimonies
1. User submits testimony
2. Email sent to your church email
3. You review in admin panel
4. Click "Approve" or "Reject"
5. Approved testimonies appear on website

### Donations
1. User sees bank details (Ecobank)
2. User transfers money
3. User fills form with transaction reference
4. User uploads receipt screenshot
5. You receive email notification
6. You verify in admin panel
7. System sends confirmation email to donor

### Contact Form
1. User sends message
2. Auto-reply sent to user
3. Email notification sent to you
4. You can mark as "read" or "replied" in admin

## Customization

### Update Church Information

Go to Admin → Church Settings and update:
- Site name and tagline
- Phone numbers
- Email addresses
- Physical address
- Social media links
- Service times

### Add Bible Verses

Go to Admin → Bible Verses → Add Bible Verse
- Enter verse text
- Enter reference (e.g., "John 3:16")
- Mark as active

Verses rotate daily on the homepage.

### Add Ministries

Go to Admin → Ministries → Add Ministry
- Ministry name
- Description
- Leader name
- Meeting schedule
- Icon class (Font Awesome icon)

### Create Events

Go to Admin → Events → Add Event
- Title and description
- Event type (service, prayer, youth, etc.)
- Date and time
- Location
- Recurring pattern (optional)

## Production Deployment

### Security Checklist

1. ✅ Change DEBUG to False in `.env`
2. ✅ Set strong SECRET_KEY
3. ✅ Update ALLOWED_HOSTS
4. ✅ Use PostgreSQL instead of SQLite
5. ✅ Enable HTTPS
6. ✅ Set secure cookie settings
7. ✅ Change admin password

### Deploy to Heroku (Example)

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create wopbic

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
# ... set all other env variables

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py setup_church

# Create superuser
heroku run python manage.py createsuperuser
```

## Troubleshooting

### Emails Not Sending

1. Check email settings in `.env`
2. Verify app password is correct
3. Check spam folder
4. Enable "Less secure app access" (Gmail)
5. Check Django logs for errors

### Images Not Showing

1. Ensure images are in `static/images/`
2. Run: `python manage.py collectstatic`
3. Check image file names match exactly

### Database Errors

```bash
# Reset database
python manage.py flush
python manage.py migrate
python manage.py setup_church
```

### Port Already in Use

```bash
# Use different port
python manage.py runserver 8080
```

## Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Email: developer@wopbic.org

## License

© 2025 World of Prayer Bible International Church

---

**Built with Django 4.2.7**