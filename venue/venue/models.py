import uuid
import requests

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Venue(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    capacity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Show(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
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


@receiver(post_save, sender=Show)
def create_tickets(sender, instance, created, **kwargs):
    if created:
        Ticket.objects.bulk_create(
            [Ticket(show=instance) for i in range(instance.venue.capacity)],
            batch_size=instance.venue.capacity,
        )


class Ticket(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    sold = models.BooleanField(default=False)
    scanned = models.BooleanField(default=False)
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




