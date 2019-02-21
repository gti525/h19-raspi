import uuid
import requests

from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    capacity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Show(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        related_name="shows",
    )
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.name} | {self.venue}'


class Ticket(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    sold = models.BooleanField()
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ticket {self.uuid} for {self.show}'


class Seller(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f'{self.name} - {self.url}'

    # def send_show_to_url(self, show):
    #     show = Show.objects.get(id=show)

    #     serializer = ShowTicketSerializer(data=show)

    #     response = requests.post(
    #         self.url,
    #         serializer.data
    #     )

    #     return response




