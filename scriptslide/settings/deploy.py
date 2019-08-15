from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'scriptslide-rds.cavrmrh2ww2x.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'NAME': 'scriptslide',
        'USER': 'jihoon',
        'PASSWORD': 'rkdwlgns0522',
    }
}