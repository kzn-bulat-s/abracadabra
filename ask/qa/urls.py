from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.test),    
    url(r'^login/$', views.test),    
    url(r'^signup/$', views.test),    
    url(r'^question/\d+/$', views.test),    
    url(r'^ask/$', views.test),    
    url(r'^popular/$', views.test),    
    url(r'^new/$', views.test),    
]
