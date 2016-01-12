# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

class Document(models.Model):
  docfile = models.FileField(upload_to='images')