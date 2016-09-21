from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)

from .models import LabPublication

class LabPublicationForm(forms.ModelForm):
    class Meta:
        model = LabPublication
        fields = ('user', 'title', 'authors', 'journal', 'year', 'journal_url', 'pubmed', 'citation', 'mini_citation', 'abstract', 'pdf', 'picture')
