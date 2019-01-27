from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'api/video', views.upload_video, name='video'),
    url(r'api/apply', views.apply_actions, name='apply'),
]
