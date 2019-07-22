
from django.conf.urls import url
from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/control/<speech_script_id>/', consumers.ChatConsumer),
]