from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_questions),
    url(r'^login/$', views.login),    
    url(r'^signup/$', views.signup),    
    url(r'^question/(?P<id>\d+)/$', views.show_question, name='question'),
    url(r'^ask/$', views.ask_question, name='ask'),    
    url(r'^popular/$', views.list_popular_questions),    
    url(r'^new/$', views.list_questions),    
]
