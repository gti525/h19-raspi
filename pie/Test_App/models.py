import uuid
from django.db import models

# Create your models here.


class Tech(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    name2 = models.CharField(max_length=100)


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_name = models.CharField(max_length=10, default='Test')
