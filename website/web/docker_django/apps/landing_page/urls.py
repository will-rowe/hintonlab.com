from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='landing_page'),
    url(r'^the-team$', views.the_team, name='the_team'),
    url(r'^research$', views.research, name='research'),
    url(r'^tools$', views.tools, name='tools'),
    url(r'^publications$', views.publications, name='publications'),
    url(r'^publication/(?P<pk>\d+)/$', views.publication_detail, name='publication_detail'),
    url(r'^publication/(?P<pk>\d+)/edit/$', views.edit_publication, name='edit_publication'),
    url(r'^publication/(?P<pk>\d+)/remove/$', views.remove_publication, name='remove_publication'),
    url(r'^pubmed_search$', views.pubmed_search, name='pubmed_search'),
    url(r'^member$', views.member, name='member'),
    url(r'^member/edit-profile/$', views.edit_profile, name='edit_profile'),
    url(r'^member/analysis$', views.analysis, name='analysis'),
]
