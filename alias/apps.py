from django.apps import AppConfig
import time
from datetime import datetime

class AliasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alias'
    # def ready(self):
    #     from .models import Alias
    #     while True:
    #         for player in Alias.objects.all():
    #             if (datetime.now() - player.lasttime).total_seconds() > 300:
    #                 player.delete()
    #         time.sleep(2)
