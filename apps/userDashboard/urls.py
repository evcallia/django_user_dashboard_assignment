from django.conf.urls import url
from . import views                   #add this line

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^login$', views.login, name='login'),
  url(r'^register$', views.register, name='register'),
  url(r'^dashboard$', views.dashboard, name='dashboard'),
  url(r'^new$', views.new, name='new'),
  url(r'^proc_login$', views.process_login, name='proc_login'),
  url(r'^create$', views.create, name='create'),
  url(r'^show(?P<id>\d+)$', views.show, name='show'),
  url(r'^edit(?P<id>\d+)$', views.edit, name='edit'),
  url(r'^remove(?P<id>\d+)$', views.remove, name='remove'),
  url(r'^log-off$', views.log_off, name='log-off'),
  url(r'^update$', views.update, name='update'),
  url(r'^message$', views.message, name='message'),
  url(r'^comment$', views.comment, name='comment'),
]


# namesake='dashboard'
