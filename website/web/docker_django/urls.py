from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('docker_django.apps.landing_page.urls')),
    url(r'^databases/', include('docker_django.apps.databases.urls')),
    url(r'^news/', include('docker_django.apps.news.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'landing_page/home.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^todo/', include('docker_django.apps.todo.urls')),
    )
