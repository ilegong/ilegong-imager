from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download_wx_image$', views.download_wx_image, name='download_wx_image')
]