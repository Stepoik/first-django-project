from django.db import models

class Players(models.Model):
    name = models.CharField(max_length=30)
    id_user = models.CharField(max_length=10)
    lobby = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    play = models.CharField(max_length=7)
    root = models.CharField(max_length=10)

class Specifications(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    name_spec = models.CharField(max_length=100)
    spec = models.CharField(max_length=255)
    open = models.CharField(max_length=10)
