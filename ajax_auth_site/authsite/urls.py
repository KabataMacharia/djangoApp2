
from django.conf.urls import url
#from django.views.generic import TemplateView
from . import views
from authsite.views import AdminsView, StaffView, SuperUserView, UnauthView, UserLoginView, RegisterView

urlpatterns = [ 				
                url(r'^register/$', RegisterView.as_view()),
                url(r'^$', UserLoginView.as_view()),
                url(r'^login/$', UserLoginView.as_view()),                
                #url(r'restricted', views.restricted, name='restricted'),
                url(r'^logout/$', views.user_logout, name='logout'),
                url(r'^admins/$', AdminsView.as_view()),
                url(r'^staff/$', StaffView.as_view()),
                url(r'^superuser/$', SuperUserView.as_view()),
                url(r'^unauth/$', UnauthView.as_view()),
				]
