
from django.conf.urls import url
#from django.views.generic import TemplateView
from authsite.views import AdminsView, StaffView, SuperUserView, UnauthView, UserLoginView, RegisterView, UserLogoutView, AdminHomeView,UserHomeView

urlpatterns = [ 				
                url(r'^register/$', RegisterView.as_view()),
                url(r'^$', UserLoginView.as_view()),
                url(r'^login/$', UserLoginView.as_view()),                
                #url(r'restricted', views.restricted, name='restricted'),
                url(r'^logout/$', UserLogoutView.as_view()),
                url(r'^admins/$', AdminsView.as_view()),
                url(r'^staff/$', StaffView.as_view()),
                url(r'^superuser/$', SuperUserView.as_view()),
                url(r'^unauth/$', UnauthView.as_view()),
                url(r'^userhome/$', UserHomeView.as_view()),
                url(r'^adminhome/$', AdminHomeView.as_view()),
                
				]
