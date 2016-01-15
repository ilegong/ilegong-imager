from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .forms import *
from .models import *
from django.conf import settings
from os import listdir
from os.path import isfile, join
import urllib2, uuid, os, json, logging, glob
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
  return HttpResponse("Hello, world. You're at the polls index.")

def download_wx_image(request):
  now = timezone.now()
  url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(request.GET['access_token'], request.GET['media_id'])
  # url = 'http://51daifan-images.stor.sinaapp.com/D11lszUt2x8ch1jZT9adeRqxJqvLmYBhEevywDIWKUA5lM6dICy6L5orKiOwL652.jpg';
  try:
    response = urllib2.urlopen(url)
    if response.getcode() != 200:
      logger.warn('Failed to download wx image, response code: %s' % response.getcode())
      return JsonResponse({'result': False, 'reason': 'response code %s' % response.getcode()})

    if response.info()['Content-Type'] == 'text/plain':
      error = response.read(int(response.info()['Content-Length']))
      error_json = json.loads(error)
      logger.warn('Failed to download wx image, reason: %s' % error)
      return JsonResponse({'result': False, 'code': error_json['errcode'], 'message': error_json['errmsg']})
  except urllib2.URLError, e:
    logger.warn('Failed to download wx image, error: %s' % str(e))
    return JsonResponse({'result': False, 'code':'URLError', 'message': e})

  filename = '%s.jpg' % uuid.uuid1()
  relative_directory = 'images/%d/%02d/%02d' % (now.year, now.month, now.day)
  absolute_directory = '%s/%s' % (settings.STORAGE_ROOT, relative_directory)
  image_url = '%s/%s'%(relative_directory, filename)

  if not os.path.exists(absolute_directory):
    os.makedirs(absolute_directory)

  with open('%s/%s' % (absolute_directory, filename), "wb") as code:
    code.write(response.read())
    logger.info('download wx image: %s, save as: %s' % (request.GET['media_id'], image_url))

  return JsonResponse({'result': True, 'url': image_url})

def upload(request):
  image_locations = '%s/images'% settings.STORAGE_ROOT
  if request.method == "GET":
    form = DocumentForm()
  else:
    form = DocumentForm(request.POST, request.FILES)
    for file in request.FILES.getlist('images'):
      name = '%s.jpg' % uuid.uuid1()
      logger.info('try to upload image %s to images/%s' % (file.name, name))
      with open('%s/%s' % (image_locations, name), "wb") as local_image:
        for chunk in file.chunks():
            local_image.write(chunk)
        logger.info('upload image %s to images/%s successfully' % (file.name, name))
    return redirect('imager:upload')

  images = filter(os.path.isfile, glob.glob(image_locations + "/*"))
  images.sort(key=lambda x: os.path.getmtime(x))
  return render(request,'imager/upload.html',{'images': images, 'form': form})
