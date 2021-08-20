from django.db import models
from django.contrib.sessions.models import Session

class Players(models.Model):
    name = models.CharField(max_length=30)
    id_user = models.CharField(max_length=10)
    lobby = models.CharField(max_length=100)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    play = models.BooleanField()
    root = models.BooleanField()
    queue = models.IntegerField()
    online = models.BooleanField()


class Specifications(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    name_spec = models.CharField(max_length=100)
    spec = models.CharField(max_length=255)
    open = models.BooleanField()
    lobby = models.CharField(max_length=255)

class Game(models.Model):
    start = models.BooleanField()
    lobby = models.CharField(max_length=255)
    bunker_size = models.CharField(max_length=255, null=True)
    bunker_kata = models.CharField(max_length=300, null=True)
    bunker_pop = models.CharField(max_length=255, null=True)
    bunker_time = models.CharField(max_length=255, null=True)

