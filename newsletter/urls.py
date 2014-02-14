from django.conf.urls import patterns, url
from newsletter import views

urlpatterns = patterns('newsletter.views',
        url(r'^(?P<item_pk>\d+)/edit/$', views.edit_item, name='edit_item'),
        url(r'^(?P<item_pk>\d+)/save/$', views.save_item, name='save_item'),
        url(r'^(?P<item_pk>\d+)/$', views.view_item, name='view_item'),
        url(r'$', views.home, name='home'),
)
