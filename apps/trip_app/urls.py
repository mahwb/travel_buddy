from django.conf.urls import url
from . import views

app_name="trip"
urlpatterns = [
    url(r'^$', views.index, name="idx"),
    url(r'^add$', views.add, name="add"),
    url(r'^add/new$', views.new, name="new"),      
    url(r'^destination/(?P<id>\d+)$', views.dest, name="dest"),
    url(r'^join/(?P<id>\d+)$', views.join, name="join"),
]
