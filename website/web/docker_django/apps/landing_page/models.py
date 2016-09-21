from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



#########################################################################################################
# site wide announcements
LEVEL_CHOICES = (
     ('warning', 'Warning'),
     ('danger', 'Danger'),
     ('success', 'Success'),
     ('info', 'Info'),
)
class Announcement(models.Model):
    """
    Model to hold global announcements
    """
    body = models.TextField(blank=False)
    display = models.BooleanField(default=False)
    level = models.CharField(max_length=8, choices=LEVEL_CHOICES, default='info')

    def __unicode__(self):
        return self.body[:50]


#########################################################################################################
# research strands
GOAL_CHOICES = (
     ('A', 'goal A'),
     ('B', 'goal B'),
     ('C', 'goal C'),
     ('D', 'goal D'),
)
class ResearchStrand(models.Model):
    user = models.ForeignKey('auth.User')
    picture = models.ImageField(upload_to='research_strand_imgs', blank=False)
    picture_tag = models.CharField(max_length=200, null=True, blank=False)
    title = models.CharField(max_length=200, null=True, blank=False)
    text = models.TextField(null=True, blank=False)
    upload_date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"), blank=False)
    goal = models.CharField(max_length=1, choices=GOAL_CHOICES, unique=True, blank=True, null=True)

    def __unicode__(self):
        return "{0}".format(self.user.username)


#########################################################################################################
# carousel
class Carousel(models.Model):
    user = models.ForeignKey('auth.User')
    picture = models.ImageField(upload_to='carousel_imgs', blank=False)
    link = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=False)
    text = models.TextField(null=True, blank=False)
    upload_date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"), blank=False)

    def __unicode__(self):
        return "{0}".format(self.user.username)


#########################################################################################################
# publications
from django.utils import timezone
class LabPublication(models.Model):
    user = models.ForeignKey('auth.User')
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=500)
    journal = models.CharField(max_length=300)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    journal_url = models.URLField(max_length=200, null=True, blank=True)
    pubmed = models.URLField(max_length=200, null=True, blank=True)
    citation = models.TextField(null=True, blank=True)
    mini_citation = models.TextField(null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    pdf = models.FileField(upload_to='lab_publications', blank=True)
    picture = models.ImageField(upload_to='lab_publications/img', blank=True)

    def __str__(self):
        return self.title


#########################################################################################################
# user profile
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='lab_profile_imgs', blank=False)
    position = models.CharField(max_length=100, null=True, blank=False)
    bio = models.TextField(null=True, blank=False)
    start_date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"), blank=False)
    end_date = models.DateField(default='2020-01-01', blank=False)

    def __unicode__(self):
        return "{0}".format(self.user.username)


#########################################################################################################
# user profile forms etc.
from django import forms
from django.forms import ModelForm
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserForm, self).__init__(*args, **kwargs)
        # set required fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['groups'].required = True

    class Meta:
            model = User
            fields = ["username", "password", "email", "first_name", "last_name", "groups"]
            error_messages = {
                'password': {
                            'max_length': ("This password is too long!"),
                            },
            }

class UserProfileForm(forms.ModelForm):
        class Meta:
                model = UserProfile
                fields = ["position", "picture", "bio"]
                help_texts = {
                    'picture': ('Please select a pre-cropped photo / photo centred on you.'),
                    'bio': ('Please enter a short biography for the site (500 characters maximum).'),
                }
                error_messages = {
                    'bio': {
                                'max_length': ("The bio is too long! Maximum length = 500 characters"),
                                },
                }


#########################################################################################################
# bioinformatic analyses
class Bioinformatics(models.Model):
    user = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=300)
    end_user = models.CharField(max_length=300)
    link = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

#########################################################################################################
# tools
class Tools(models.Model):
    user = models.ForeignKey('auth.User')
    picture = models.ImageField(upload_to='research_strand_imgs', blank=False)
    picture_tag = models.CharField(max_length=200, null=True, blank=False)
    title = models.CharField(max_length=200, null=True, blank=False)
    text = models.TextField(null=True, blank=False)
    link = models.URLField(max_length=200, null=True, blank=True)
    upload_date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"), blank=False)

    def __unicode__(self):
        return "{0}".format(self.user.username)
