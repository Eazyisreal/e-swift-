from django import forms
from properties.models import *


class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField()
    
    
class InspectionBookingForm(forms.Form):
    name = forms.CharField( max_length=100)
    email = forms.EmailField()
    phone_number = forms.IntegerField() 
    message = forms.CharField(widget=forms.Textarea)
    
    
class ContactForm(forms.Form):
    name = forms.CharField( max_length=100)
    email = forms.EmailField()
    phone_number = forms.IntegerField(required=False) 
    subject = forms.CharField( max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        
class ProjectContactForm(forms.Form):
    name = forms.CharField( max_length=100)
    email = forms.EmailField()
    phone_number = forms.IntegerField(required=False) 
    message = forms.CharField(widget=forms.Textarea)


        
class ReviewForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)