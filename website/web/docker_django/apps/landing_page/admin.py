from django.contrib import admin
from .models import UserProfile, ResearchStrand, LabPublication, Announcement, Carousel, Bioinformatics, Tools

admin.site.register(UserProfile)
admin.site.register(ResearchStrand)
admin.site.register(LabPublication)
admin.site.register(Carousel)
admin.site.register(Bioinformatics)
admin.site.register(Tools)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('body', 'level', 'display')
