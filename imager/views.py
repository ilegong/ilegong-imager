from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import urllib2, uuid, os


# Create your views here.
def index(request):
  return HttpResponse("Hello, world. You're at the polls index.")

def download_wx_image(request):
  now = timezone.now()
  url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(request.GET['access_token'], request.GET['media_id'])
  # url = 'http://51daifan-images.stor.sinaapp.com/D11lszUt2x8ch1jZT9adeRqxJqvLmYBhEevywDIWKUA5lM6dICy6L5orKiOwL652.jpg';
  response = urllib2.urlopen(url)

  directory = '/storage/images/%d/%02d/%02d' % (now.year, now.month, now.day)
  filename = '%s.jpg' % uuid.uuid1()

  if not os.path.exists(directory):
    os.makedirs(directory)

  with open('%s/%s' % (directory, filename), "wb") as code:
    code.write(response.read()) 
  return JsonResponse({'result': True, 'filename': filename})