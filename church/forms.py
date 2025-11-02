# church/forms.py
from django import forms
from django.core.validators import EmailValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import PrayerRequest, Testimony, ContactMessage, Donation, Newsletter


class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'request_text', 'privacy']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com (optional)'
            }),
            'request_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your prayer request...',
                'rows': 5
            }),
            'privacy': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'request_text': 'Prayer Request',
            'privacy': 'Privacy Setting'
        }
        help_texts = {
            'email': 'Optional - Leave blank if you prefer to remain anonymous',
            'privacy': 'Private requests are only seen by our prayer team'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'request_text',
            'privacy',
            HTML('<hr>'),
            Submit('submit', 'Submit Prayer Request', css_class='btn btn-primary btn-block')
        )


class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimony
        fields = ['name', 'title', 'story']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., God\'s Healing Power in My Life'
            }),
            'story': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us what God has done in your life...',
                'rows': 8
            })
        }
        labels = {
            'title': 'Testimony Title',
            'story': 'Your Testimony'
        }
        help_texts = {
            'story': 'Please share your testimony in detail. All testimonies are reviewed before publication.'
        }

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    from django.conf import settings
    bank = settings.CHURCH_BANK_DETAILS
    
    self.helper = FormHelper()
    self.helper.layout = Layout(
        HTML(f'<div class="alert alert-info">'
             f'<h5><i class="fas fa-university"></i> Bank Details</h5>'
             f'<p><strong>Bank:</strong> {bank["BANK_NAME"]}<br>'
             f'<strong>Account Name:</strong> {bank["ACCOUNT_NAME"]}<br>'
             f'<strong>Account Number:</strong> {bank["ACCOUNT_NUMBER"]}<br>'
             f'<p class="mb-0"><small>After making your transfer, please fill out this form to confirm your donation.</small></p>'
             '</div>'),
        Row(
            Column('donor_name', css_class='form-group col-md-6 mb-3'),
            Column('donor_email', css_class='form-group col-md-6 mb-3'),
            css_class='form-row'
        ),
        Row(
            Column('donor_phone', css_class='form-group col-md-6 mb-3'),
            Column('donation_type', css_class='form-group col-md-6 mb-3'),
            css_class='form-row'
        ),
        Row(
            Column('amount', css_class='form-group col-md-6 mb-3'),
            Column('confirm_amount', css_class='form-group col-md-6 mb-3'),
            css_class='form-row'
        ),
        'transaction_reference',
        'receipt_image',
        HTML('<div class="alert alert-warning mt-3">'
             '<i class="fas fa-exclamation-triangle"></i> '
             'Please ensure all information is accurate. Your donation will be verified by our finance team.'
             '</div>'),
        Submit('submit', 'Submit Donation Details', css_class='btn btn-primary btn-block mt-3')
    )

class DonationForm(forms.ModelForm):
    confirm_amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        }),
        help_text='Please confirm the amount you transferred'
    )

    class Meta:
        model = Donation
        fields = ['donor_name', 'donor_email', 'donor_phone', 'donation_type', 
                  'amount', 'transaction_reference', 'receipt_image']
        widgets = {
            'donor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'donor_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'donor_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+234 XXX XXX XXXX'
            }),
            'donation_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'transaction_reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Transaction reference from your bank'
            }),
            'receipt_image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
        }
        labels = {
            'donor_name': 'Full Name',
            'donor_email': 'Email Address',
            'donor_phone': 'Phone Number',
            'donation_type': 'Type of Giving',
            'amount': 'Amount (₦)',
            'transaction_reference': 'Transaction Reference',
            'receipt_image': 'Upload Receipt/Screenshot'
        }
        help_texts = {
            'donor_phone': 'Optional - For confirmation purposes',
            'transaction_reference': 'Enter the reference number from your bank transfer',
            'receipt_image': 'Upload a screenshot or photo of your transfer receipt'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<div class="alert alert-info">'
                 '<h5><i class="fas fa-university"></i> Bank Details</h5>'
                 '<p><strong>Bank:</strong> Ecobank<br>'
                 '<strong>Account Name:</strong> World of prayer Bible intl, church<br>'
                 '<strong>Account Number:</strong> 3802032384<br>'
                 '<p class="mb-0"><small>After making your transfer, please fill out this form to confirm your donation.</small></p>'
                 '</div>'),
            Row(
                Column('donor_name', css_class='form-group col-md-6 mb-3'),
                Column('donor_email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('donor_phone', css_class='form-group col-md-6 mb-3'),
                Column('donation_type', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('amount', css_class='form-group col-md-6 mb-3'),
                Column('confirm_amount', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'transaction_reference',
            'receipt_image',
            HTML('<div class="alert alert-warning mt-3">'
                 '<i class="fas fa-exclamation-triangle"></i> '
                 'Please ensure all information is accurate. Your donation will be verified by our finance team.'
                 '</div>'),
            Submit('submit', 'Submit Donation Details', css_class='btn btn-primary btn-block mt-3')
        )

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        confirm_amount = cleaned_data.get('confirm_amount')

        if amount and confirm_amount:
            if amount != confirm_amount:
                raise forms.ValidationError(
                    "The amount and confirmation amount must match."
                )

        return cleaned_data


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-md-8'),
                Column(Submit('submit', 'Subscribe', css_class='btn btn-primary'), css_class='col-md-4'),
                css_class='form-row'
            )
        )


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search sermons, events, testimonies...'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('query', css_class='col-md-10'),
                Column(Submit('submit', 'Search', css_class='btn btn-primary'), css_class='col-md-2'),
                css_class='form-row'
            )
        )
        
        from django import forms

class ContactForm(forms.Form):
    Full_Name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
