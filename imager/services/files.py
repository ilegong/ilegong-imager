#coding:utf-8
import os, logging
from django.conf import settings
from django.utils import timezone
import urllib2, uuid, os, json, logging, glob
logger = logging.getLogger(__name__)

def ensure_directory(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)
  return directory

def download_image(url, category, filename):
  try:
    response = urllib2.urlopen(url)
    if response.getcode() != 200:
      logger.warn('Failed to download image, response code: %s' % response.getcode())
      raise Exception('response code %s' % response.getcode())

    if response.info()['Content-Type'] == 'text/plain':
      error = response.read(int(response.info()['Content-Length']))
      if 1 == 1:
        error_json = json.loads(error)
        raise Exception('code %s, message %s' % (error_json['errcode'], error_json['errmsg']))
      else:
        raise Exception('Not an image')
  except urllib2.URLError, e:
    raise Exception('URLError: %s' % e)
  except ValueError, e:
    raise Exception('ValueError: %s' % e)

  now = timezone.now()
  relative_directory = '%s/%d/%02d/%02d' % (category, now.year, now.month, now.day)
  absolute_directory = ensure_directory('%s/%s' % (settings.STORAGE_ROOT, relative_directory))

  image = '%s/%s' % (absolute_directory, filename)
  with open(image, "wb") as code:
    code.write(response.read())
    return '%s/%s'%(relative_directory, filename)

def save_images_with_file_streams(files, category, filename):
  now = timezone.now()
  relative_directory = '%s/%d/%02d/%02d' % (category, now.year, now.month, now.day)
  absolute_directory = ensure_directory('%s/%s' % (settings.STORAGE_ROOT, relative_directory))

  image_urls = []
  try:
    for file in files:
      image_url = '%s/%s' % (relative_directory, filename)
      image_urls.append(image_url)
      logger.info('try to upload image %s to %s' % (file.name, image_url))
      image = '%s/%s' % (absolute_directory, filename)
      with open(image, "wb") as local_image:
        for chunk in file.chunks():
            local_image.write(chunk)
        logger.info('upload image %s to %s successfully' % (file.name, image_url))
  except IOError, e:
    raise Exception('IOError: %s' % e)

  return image_urls

def save_images_with_raw_data(raw_data, category, filename):
  now = timezone.now()
  relative_directory = '%s/%d/%02d/%02d' % (category, now.year, now.month, now.day)
  absolute_directory = ensure_directory('%s/%s' % (settings.STORAGE_ROOT, relative_directory))

  try:
    image_url = '%s/%s' % (relative_directory, filename)
    logger.info('try to upload image of raw data to %s' % image_url)
    image = '%s/%s' % (absolute_directory, filename)
    with open(image, "wb") as local_image:
      local_image.write(raw_data)
      logger.info('upload image of raw data to %s successfully' % image_url)
    return image_url
  except IOError, e:
    raise Exception('IOError: %s' % e)
