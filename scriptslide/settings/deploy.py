from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    '172.31.47.251',
    '.scriptslide.com',
    '.amazonaws.com',
]

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