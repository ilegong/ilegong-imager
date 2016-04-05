from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
from services.images import *
from services.files import *
from django.conf import settings
from os import listdir
from os.path import isfile, join
import urllib2, uuid, os, json, logging, glob, base64
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
  return HttpResponse("Hello, world.")

# download images from given urls and write to a specific directory
# download_wx_image and download_avatar could be replaced by this function
# POST, url, directory, 
@csrf_exempt
def download_image_to(request):
  now = timezone.now()
  if request.method == "GET":
    return HttpResponseNotAllowed('Only POST here')

  token = request.POST['token'];
  if 'PYS_IMAGES_001' != token: 
    return HttpResponseForbidden('Forbidden')

  if 'url' not in request.POST or 'category' not in request.POST:
    return HttpResponseBadRequest('Please provide url and category')

  try:
    if 'filename' in request.POST:
      filename = request.POST['filename'] if request.POST['filename'].rfind('.') >0 else '%s.jpg'%request.POST['filename'];
    else :
      filename = '%s.jpg' % uuid.uuid1()

    image_url = download_image(request.POST['url'], request.POST['category'], filename)
    logger.info('download image: %s, save as: %s' % (request.POST['url'], image_url))
    return JsonResponse({'result': True, 'url': image_url})
  except Exception, e:
    logger.warn('Failed to download image, error: %s' % str(e))
    return JsonResponse({'result': False, 'message': str(e)})
  
# download images from wx by media_id and access_token
@csrf_exempt
def download_wx_image(request):
  now = timezone.now()
  if request.method == "GET":
    url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(request.GET['access_token'], request.GET['media_id'])    
  else:
    url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(request.POST['access_token'], request.POST['media_id'])

  try:
    filename = '%s.jpg' % uuid.uuid1()

    image_url = download_image(url, 'images', filename)
    logger.info('download image: %s, save as: %s' % (request.POST['url'], image_url))
    return JsonResponse({'result': True, 'url': image_url})
  except Exception, e:
    logger.warn('Failed to download image, error: %s' % str(e))
    return JsonResponse({'result': False, 'message': str(e)})
  
# download avatar from given url
@csrf_exempt
def download_avatar(request):
  if request.method == "GET":
    return HttpResponseNotAllowed('Only POST here')
  if 'url' not in request.POST:
    return HttpResponseBadRequest('Please provide url')

  try:
    image_url = download_image(request.POST['url'], 'avatar', '%s.jpg' % uuid.uuid1())
    logger.info('download image: %s, save as: %s' % (request.POST['url'], image_url))
    return JsonResponse({'result': True, 'url': image_url})
  except Exception, e:
    logger.warn('Failed to download image, error: %s' % str(e))
    return JsonResponse({'result': False, 'message': str(e)})

# upload avatar
# upload_weshare_images and upload_index_images could be replaced by this function
# POST, url, directory, 
@csrf_exempt
def upload_images_with_base64(request):
  if request.method == "GET":
    return HttpResponseNotAllowed('Only POST here')
  if 'category' not in request.POST:
    return HttpResponseBadRequest('Please provide category')

  try:
    raw_data = base64.decodestring(request.POST['images'].split(';')[-1].split(',')[-1]);
    image_urls = save_images_with_raw_data(raw_data, request.POST['category'], '%s.jpg' % uuid.uuid1())
    logger.info(image_urls);
    return JsonResponse({'result': True, 'url': image_urls})
  except Exception, e:
    logger.warn('Failed to upload images, error: %s' % str(e))
    return JsonResponse({'result': False, 'code':'IOError', 'message': str(e)})

# upload multiple images for a weshare
@csrf_exempt
def upload_weshare_images(request):
  if request.method == "GET":
    return HttpResponseNotAllowed('Only POST here')

  try:
    image_urls = save_images_with_file_streams(request.FILES.getlist('images'), 'images', '%s.jpg' % uuid.uuid1())
    return JsonResponse({'result': True, 'url': image_urls})
  except Exception, e:
    logger.warn('Failed to upload images, error: %s' % str(e))
    return JsonResponse({'result': False, 'code':'IOError', 'message': str(e)})

# upload a pool image or index image
@csrf_exempt
def upload_index_images(request):
  if request.method == "GET":
    return redirect('/upload_images');

  try:
    image_urls = save_images_with_file_streams(request.FILES.getlist('images'), 'images/index', '%s.jpg' % uuid.uuid1())
    return JsonResponse({'result': True, 'url': image_urls})
  except Exception, e:
    logger.warn('Failed to upload images, error: %s' % str(e))
    return JsonResponse({'result': False, 'code':'IOError', 'message': str(e)})

# upload a pool image or index image
@csrf_exempt
def upload(request):
  if request.method == "GET":
    return redirect('/upload_images');

  try:
    image_urls = save_images_with_file_streams(request.FILES.getlist('images'), 'images/index', '%s.jpg' % uuid.uuid1())
    return JsonResponse({'result': True, 'url': image_urls})
  except Exception, e:
    logger.warn('Failed to upload images, error: %s' % str(e))
    return JsonResponse({'result': False, 'code':'IOError', 'message': str(e)})

# list images that uploaded before
def upload_images(request):
  relative_directory = 'images/index'
  absolute_directory = '%s/%s' % (settings.STORAGE_ROOT, relative_directory)
  form = DocumentForm()

  images = filter(os.path.isfile, glob.glob(absolute_directory + "/*"))
  images.sort(key=lambda x: os.path.getmtime(x))
  images.reverse()
  images = [x.replace('%s/' % settings.STORAGE_ROOT, '') for x in images]
  return render(request,'imager/upload_images.html',{'images': images, 'form': form})
