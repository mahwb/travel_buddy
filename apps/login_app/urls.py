from django.conf.urls import url
from . import views

app_name="login"
urlpatterns = [
    url(r'^$', views.index, name="idx"),
    url(r'^register$', views.register, name="reg"),
    url(r'^login$', views.login, name="li"),
    url(r'^logout$', views.logout, name="lo"),
]