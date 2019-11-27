from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    '13.125.157.168',
    '172.31.25.145',
    '.scriptslide.net',
    '.scriptslide.com',
    '.amazonaws.com',
]




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'rds-mysql.c4xnvy7goexk.ap-northeast-2.rds.amazonaws.com',
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
            "hosts": [('server-redis-001.8tdxoe.0001.apn2.cache.amazonaws.com', 6379)],
        },
        'group_expiry': 60 * 60 * 3,
        'expiry': 60
    },
}