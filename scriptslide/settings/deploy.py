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
        'CONN_MAX_AGE': None,
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('django-redis-001.z4ud64.0001.apn2.cache.amazonaws.com', 6379)],
        },
        'group_expiry': 60 * 60 * 3,  # 3시간
        'expiry': 60  # 60초
    },
}