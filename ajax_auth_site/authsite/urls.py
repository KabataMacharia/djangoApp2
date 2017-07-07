
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views


urlpatterns = [ 				
                url(r'^register/$', views.register, name='register'),
                url(r'^$', views.user_login, name='login'),
                url(r'^login/$', views.user_login, name='login'),                
                #url(r'restricted', views.restricted, name='restricted'),
                url(r'^logout/$', views.user_logout, name='logout'),
                url(r'^admins/$', TemplateView.as_view(template_name='authsite/admin.html')),
                url(r'^staff/$', TemplateView.as_view(template_name='authsite/staff.html')),
                url(r'^superuser/$', TemplateView.as_view(template_name='authsite/superuser.html')),
                url(r'^unauth/$', TemplateView.as_view(template_name='authsite/unauth.html')),
				]
