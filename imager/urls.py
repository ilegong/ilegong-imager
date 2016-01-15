from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download_wx_image$', views.download_wx_image, name='download_wx_image'),
    url(r'^download_wx_avatar$', views.download_wx_avatar, name='download_wx_avatar'),
    url(r'^upload$', views.upload, name='upload')
]