from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.home, name='databases'),
    url(r'^mutant-database/$', views.mutant_database, name='mutant-database'),
    url(r'^mutant-database/MUTANT-search/$', views.MUTANT_search, name='MUTANT-search'),
]
