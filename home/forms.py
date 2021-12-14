
from django.forms import ModelForm, TextInput, Textarea, EmailInput
from .models import ContactMessage

class ContactMessageForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Enter name'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Enter email'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Message subject'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Write your message...'}),
        }