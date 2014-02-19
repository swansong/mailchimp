from django.conf.urls import patterns, url
from newsletter import views

urlpatterns = patterns('newsletter.views',
        url(r'^(?P<item_pk>\d+)/edit/$', views.edit_item, name='edit_item'),
        url(r'^(?P<item_pk>\d+)/$', views.view_item, name='view_item'),
        url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', views.view_date, name='view-date'),
        url(r'^new/$', views.new_item, name='new_item'),
        url(r'^home/$', views.home, name='home'),
        url(r'^feed/$', views.rss, name='rss'),
)
