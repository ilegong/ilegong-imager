from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download_wx_image$', views.download_wx_image, name='download_wx_image'),
    url(r'^download_avatar$', views.download_avatar, name='download_avatar'),
    url(r'^download_image_from$', views.download_image_from, name='download_image_from'),
    url(r'^upload_images_with_base64$', views.upload_images_with_base64, name='upload_images_with_base64'),
    url(r'^upload_images_to$', views.upload_images_to, name='upload_images_to'),
    url(r'^upload_weshare_images$', views.upload_weshare_images, name='upload_weshare_images'),
    url(r'^images_index$', views.images_index, name='images_index'),
    url(r'^upload$', views.upload, name='upload')
]