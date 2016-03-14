from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseNotAllowed
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
from services.images import *
from services.files import *
from django.conf import settings
from os import listdir
from os.path import isfile, join
import urllib2, uuid, os, json, logging, glob
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
  return HttpResponse("Hello, world.")

@csrf_exempt
def download_wx_image(request):
  now = timezone.now()
  if request.method == "GET":
    url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(request.GET['access_token'], request.GET['media_id'])    
  else:
    url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(request.POST['access_token'], request.POST['media_id'])

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
  except ValueError, e:
    logger.warn('Failed to download wx image %s, error: %s' % (url, str(e)))
    return JsonResponse({'result': False, 'code':'ValueError', 'message': e})

  filename = '%s.jpg' % uuid.uuid1()
  relative_directory = 'images/%d/%02d/%02d' % (now.year, now.month, now.day)
  absolute_directory = ensure_directory('%s/%s' % (settings.STORAGE_ROOT, relative_directory))

  image = '%s/%s' % (absolute_directory, filename)
  with open(image, "wb") as code:
    code.write(response.read())
    logger.info('download wx image: %s, save as: %s' % (request.GET['media_id'], image))
  
  compress_image_to(image, ensure_directory('%s/images/m/%d/%02d/%02d/' % (settings.STORAGE_ROOT, now.year, now.month, now.day)), 150, 150)
  compress_image_to(image, ensure_directory('%s/images/s/%d/%02d/%02d/' % (settings.STORAGE_ROOT, now.year, now.month, now.day)), 80, 80)

  return JsonResponse({'result': True, 'url': '%s/%s'%(relative_directory, filename)})

@csrf_exempt
def download_avatar(request):
  if request.method == "GET":
    return HttpResponseNotAllowed('Only POST here')

  now = timezone.now()
  url = request.POST['url'];
  logger.debug('Start to download avatar %s' % url)
  try:
    response = urllib2.urlopen(url)
    if response.getcode() != 200:
      logger.warn('Failed to download avatar %s, response code: %s' % (url, response.getcode()))
      return JsonResponse({'result': False, 'reason': 'response code %s' % response.getcode()})

  except urllib2.URLError, e:
    logger.warn('Failed to download avatar %s, error: %s' % (url, str(e)))
    return JsonResponse({'result': False, 'code':'URLError', 'message': e})
  except ValueError, e:
    logger.warn('Failed to download avatar %s, error: %s' % (url, str(e)))
    return JsonResponse({'result': False, 'code':'ValueError', 'message': e})

  filename = 'wx_head_%s.jpg' % uuid.uuid1()
  relative_directory = 'avatar/%d/%02d/%02d' % (now.year, now.month, now.day)
  absolute_directory = ensure_directory('%s/%s' % (settings.STORAGE_ROOT, relative_directory))

  image = '%s/%s' % (absolute_directory, filename)
  with open(image, "wb") as code:
    code.write(response.read())
    logger.info('download avatar: %s, save as: %s' % (url, image))
  compress_image_to(image, ensure_directory('%s/avatar/m/%d/%02d/%02d/' % (settings.STORAGE_ROOT, now.year, now.month, now.day)), 150, 150)
  compress_image_to(image, ensure_directory('%s/avatar/s/%d/%02d/%02d/' % (settings.STORAGE_ROOT, now.year, now.month, now.day)), 80, 80)

  return JsonResponse({'result': True, 'url': '%s/%s'%(relative_directory, filename)})

@csrf_exempt
def upload_weshare_images(request):
  if request.method == "GET":
    return HttpResponseNotAllowed('Only POST here')

  now = timezone.now()
  relative_directory = 'images/%d/%02d/%02d' % (now.year, now.month, now.day)
  absolute_directory = ensure_directory('%s/%s' % (settings.STORAGE_ROOT, relative_directory))

  image_urls = []
  try:
    form = DocumentForm(request.POST, request.FILES)
    for file in request.FILES.getlist('images'):
      filename = '%s.jpg' % uuid.uuid1()
      image_url = '%s/%s' % (relative_directory, filename)
      image_urls.append(image_url)
      logger.info('try to upload image %s to %s' % (file.name, image_url))
      image = '%s/%s' % (absolute_directory, filename)
      with open(image, "wb") as local_image:
        for chunk in file.chunks():
            local_image.write(chunk)
        logger.info('upload image %s to %s successfully' % (file.name, image_url))
      compress_image_to(image, ensure_directory('%s/images/m/%d/%02d/%02d/' % (settings.STORAGE_ROOT, now.year, now.month, now.day)), 150, 150)
      compress_image_to(image, ensure_directory('%s/images/s/%d/%02d/%02d/' % (settings.STORAGE_ROOT, now.year, now.month, now.day)), 80, 80)
  except IOError, e:
    logger.warn('Failed to upload weshare images, error: %s' % str(e))
    return JsonResponse({'result': False, 'code':'IOError', 'message': str(e)})

  return JsonResponse({'result': True, 'url': image_urls})

def upload_images(request):
  relative_directory = 'images'
  absolute_directory = '%s/%s' % (settings.STORAGE_ROOT, relative_directory)
  form = DocumentForm()

  images = filter(os.path.isfile, glob.glob(absolute_directory + "/*"))
  images.sort(key=lambda x: os.path.getmtime(x))
  images = [os.path.basename(x) for x in images]
  return render(request,'imager/upload_images.html',{'images': images, 'form': form})

@csrf_exempt
def upload(request):
  if request.method == "GET":
    return redirect('/upload_images');

  relative_directory = 'images'
  absolute_directory = '%s/%s' % (settings.STORAGE_ROOT, relative_directory)
  image_urls = []
  try:
    form = DocumentForm(request.POST, request.FILES)
    for file in request.FILES.getlist('images'):
      filename = '%s.jpg' % uuid.uuid1()
      image_url = '%s/%s' % (relative_directory, filename)
      image_urls.append(image_url)
      logger.info('try to upload image %s to %s' % (file.name, image_url))

      with open('%s/%s' % (absolute_directory, filename), "wb") as local_image:
        for chunk in file.chunks():
            local_image.write(chunk)
        logger.info('upload image %s to %s successfully' % (file.name, image_url))
  except IOError, e:
    logger.warn('Failed to upload images, error: %s' % str(e))
    return JsonResponse({'result': False, 'code':'IOError', 'message': str(e)})

  return JsonResponse({'result': True, 'url': image_urls})
