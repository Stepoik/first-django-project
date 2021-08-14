from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/bunker/(?P<lobby>\w+)/$', consumers.PlayerConsumer.as_asgi()),
]