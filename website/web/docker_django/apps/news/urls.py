from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.news, name='news'),
    url(r'^filter-lab-news$', views.lab_news, name='lab_news'),
    url(r'^filter-social-news$', views.social_news, name='social_news'),
    url(r'^filter-other-news$', views.other_news, name='other_news'),
    url(r'^news-search/$', views.news_search, name='news_search'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]
