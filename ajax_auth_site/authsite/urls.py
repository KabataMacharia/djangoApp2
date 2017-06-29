# Derived from Talk urls
from django.conf.urls import url
from . import views


urlpatterns = [ url(r'^$',views.home, name='home'),
				url(r'^create_post/$', views.create_post, name='create_post'),
				]
