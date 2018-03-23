from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^trips$', views.trips),
    url(r'^trips/(?P<id>\d+)$', views.tripsId),
    url(r'^trips/add$', views.tripsAdd),
    url(r'^add$', views.add),
    url(r'^join/(?P<id>\d+)$', views.join),
]
