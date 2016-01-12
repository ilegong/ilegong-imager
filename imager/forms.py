# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
  docfile = forms.FileField(
    label='请选择图片',
    help_text='文件最大2M'
  )