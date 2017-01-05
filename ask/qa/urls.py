from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_questions),
    url(r'^login/$', views.test),    
    url(r'^signup/$', views.test),    
    url(r'^question/(?P<id>\d+)/$', views.show_question, name='question'),
    url(r'^ask/$', views.test),    
    url(r'^popular/$', views.list_popular_questions),    
    url(r'^new/$', views.test),    
]
