import uuid
import requests

from django.db import models

class Billet(models.Model):
    idMobile = models.CharField(max_length=150)
    idBillet = models.UUIDField()
    #date = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.sold

