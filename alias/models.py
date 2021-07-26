from django.db import models
from django.contrib.sessions.models import Session
from datetime import datetime
class Alias(models.Model):
    name = models.CharField(max_length=20)
    root = models.CharField(max_length=5)
    lobby = models.CharField(max_length=7)
    team = models.CharField(max_length=7)
    session = models.CharField(Session,db_column='session_key', max_length=100)
    ready = models.CharField(max_length=5)
class Teams(models.Model):
    team = models.CharField(max_length=7)
    lobby = models.CharField(max_length=7)
    score = models.IntegerField()
    player_quest = models.IntegerField()
class Games(models.Model):
    lobby = models.CharField(max_length=7)
    start = models.CharField(max_length=5)
    queue = models.IntegerField()
    round = models.CharField(max_length=5)
    roundend = models.DateTimeField(auto_now_add=True)
class Words(models.Model):
    word = models.CharField(max_length=50)
    lobby = models.CharField(max_length=7)
    status = models.CharField(max_length=5)

