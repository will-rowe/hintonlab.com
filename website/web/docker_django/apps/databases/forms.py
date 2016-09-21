from django.forms import ModelForm
from .models import MEETINGS

class MeetingsForm(ModelForm):
    DATE = forms.DateTimeField(input_formats=('%d.%m.%Y',))
    TIME = models.TimeField(input_formats=('%H:%M',))
    VENUE =  models.CharField()
    SPEAKER =  models.CharField()
    TOPIC = models.TextField()

    class Meta:
        model = MEETINGS
