#coding:utf-8
import os, logging
from django.conf import settings
from django.utils import timezone
import urllib2, uuid, os, json, logging, glob

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