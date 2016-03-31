from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^loadstate/$', views.load_state, name='load_state'),
]
