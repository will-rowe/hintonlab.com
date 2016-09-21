from django.db import models
from django.utils import timezone
from datetime import datetime

class NOTIFICATIONS(models.Model):
    USER = models.ForeignKey('auth.User')
    NOTIFICATION = models.TextField('NOTIFICATION', default="...")
    DATE = models.DateField('DATE', default=datetime.now().strftime("%Y-%m-%d"))

    def __unicode__(self):
        return self.name

class MUTANTS(models.Model):
    INDEX = models.CharField('INDEX', max_length=100, default=00000)
    LOCATION_IDENTIFIER = models.CharField('LOCATION_IDENTIFIER', max_length=100)
    GROUP = models.CharField('GROUP', max_length=100)
    COLLECTION_NUMBER = models.CharField('COLLECTION_NUMBER', max_length=100)
    GENOTYPE = models.TextField('GENOTYPE', default="no details available")
    CONSTRUCTION_DETAILS = models.TextField('CONSTRUCTION_DETAILS', default="no details available")
    DATE = models.CharField('DATE', default=timezone.now, max_length=100)
    LAB_MEMBER = models.CharField('LAB_MEMBER', max_length=100, default="no details available")
    GROWTH_CONDITIONS = models.TextField('GROWTH_CONDITIONS', default="no details available")
    KNOWN_AS = models.TextField('KNOWN_AS', default="no details available")
    NOTES = models.TextField('NOTES', default="no notes available")
    ADDED_TO_DB = models.DateTimeField('DATE', default=timezone.now)

    def __unicode__(self):
        return self.name

class MEETINGS(models.Model):
    DATE = models.DateField('DATE', default=datetime.now().strftime("%Y-%m-%d"))
    TIME = models.TimeField('TIME', default=datetime.now().strftime("%H:%M"))
    VENUE = models.CharField('VENUE', max_length=100, default='Committee Room')
    SPEAKER = models.CharField('SPEAKER', max_length=100, default='TBA')
    TOPIC = models.TextField('TOPIC', default="TBA")

    def __unicode__(self):
        return self.name

# register models for watson searching
from watson import search as watson
watson.register(MUTANTS, store=("GROUP", "GENOTYPE"))
watson.register(MEETINGS)
