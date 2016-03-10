#coding:utf-8
'''
    python图片处理
    @author:fc_lamp
    @blog:http://fc-lamp.blog.163.com/
'''
from PIL import Image, ImageFile
import os, logging, glob, sys, shutil, logging

logger = logging.getLogger(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True

#等比例压缩图片
def resize(**args):
    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
        
    im = Image.open(arg['ori_img'])
    ori_w,ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio
            
        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
        
    im.resize((newWidth,newHeight),Image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])

#裁剪压缩图片
def clipAndResize(ori_img, dst_img, dst_w, dst_h):        
    im = Image.open(ori_img)
    ori_w,ori_h = im.size

    dst_scale = float(dst_h) / dst_w #目标高宽比
    ori_scale = float(ori_h) / ori_w #原高宽比

    if ori_scale >= dst_scale:
        #过高
        width = ori_w
        height = int(width*dst_scale)
        x = 0
        y = (ori_h - height) / 3
    else:
        #过宽
        height = ori_h
        width = int(height*dst_scale)
        x = (ori_w - width) / 2
        y = 0

    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    #压缩
    ratio = float(dst_w) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth,newHeight),Image.ANTIALIAS).save(dst_img,quality=95)    

def compress_image_to(file, directory, width, height):
    newfile = '%s/%s' % (directory, os.path.basename(file))
    if os.path.exists(newfile):
        logger.warn('Ignore: file already exists %s' % newfile)
        return;

    try:
        logger.debug('Compress %s to %s' % (file, newfile))
        clipAndResize(file,newfile,width,height)

        if os.path.getsize(newfile) >= os.path.getsize(file):
            shutil.copyfile(file, newfile)
    except IOError, e:
        logger.warn('Failed to compress %s: %s' % (file, str(e)))
        shutil.copyfile(file, newfile)

def compressDirectory(directory):
    for file in glob.glob(directory + '/*'):
        if os.path.isdir(file):
            logger.debug('Compress images in directory %s' % os.path.abspath(file))
            compressDirectory(file)
            continue
        if file.find('_thumb') >= 0:
            continue

        compress_image_to(file, ensure_directory(directory.replace('avatar/', 'avatar/m/')), 150, 150)
        compress_image_to(file, ensure_directory(directory.replace('avatar/', 'avatar/s/')), 80, 80)

def ensure_directory(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)
  return directory

if len(sys.argv) < 2:
    logger.debug('Error: Please provide a directory')
    sys.exit(0);
if not os.path.isdir(sys.argv[1]):
    logger.debug('Error: directory %s does not exist or is not a directory.' % sys.argv[1])
    sys.exit(0);

compressDirectory(sys.argv[1])            