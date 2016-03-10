#coding:utf-8
import os, logging

def ensure_directory(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)
  return directory
