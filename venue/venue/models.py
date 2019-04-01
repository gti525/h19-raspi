import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _


from venue import clients as seller_clients


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
    artist = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    date = models.DateTimeField()
    image_url = models.CharField(max_length=250, null=True, blank=True)

    ticket_price = models.FloatField()

    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        related_name="shows",
    )

    def get_tickets(self):
        return self.ticket_set.all()

    def __str__(self):
        return f'{self.name} | {self.venue}'


@receiver(post_save, sender=Show)
def create_tickets(sender, instance, created, **kwargs):
    if created:
        Ticket.objects.bulk_create(
            [Ticket(
                show=instance,
                price=instance.ticket_price,
            ) for i in range(instance.venue.capacity)],
            batch_size=instance.venue.capacity,
        )


class Ticket(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    sold = models.BooleanField(default=False)
    scanned = models.BooleanField(default=False)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f'Ticket {self.uuid} for {self.show}'


class Seller(models.Model):
    name = models.CharField(max_length=100)
    base_url = models.CharField(max_length=150)
    token = models.CharField(max_length=150)
    active = models.BooleanField(default=True)

    client_class = models.CharField(
        max_length=100,
        choices=[
            (client, client) for client in seller_clients.__all__
        ],
    )

    def __str__(self):
        return self.name

    def get_api_client(self):
        APIClient = getattr(seller_clients, self.client_class)

        return APIClient(
            url=self.base_url,
            token=self.token,
        )

    def create_show(self, show, tickets):
        client = self.get_api_client()
        success, message = client.create_show(show, tickets)

        if not success:
            return success, message

        publication = ShowPublication.objects.create(
            show=show,
            seller=self,
            status=1,
        )

        publication.tickets.set(tickets)

        return success, 'Spectacle publié avec succès'

    def end_sale(self, show):
        client = self.get_api_client()
        success, message = client.end_sale(show)

        if not success:
            return success, message

        return success, message

    def delete_show(self, show):
        client = self.get_api_client()
        success, message = client.delete_show(show)

        if not success:
            return success, message

        return success, 'Spectacle supprimé avec succès'





class ShowPublication(models.Model):
    CREATED = 0
    ON_SALE = 1
    SALE_ENDED = 2

    STATUS = (
        (CREATED, _('CREATED')),
        (ON_SALE, _('ON SALE')),
        (SALE_ENDED, _('SALE ENDED')),
    )

    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)

    status = models.PositiveIntegerField(
        choices=STATUS,
        default=0,
    )

    def __str__(self):
        return f'[{self.seller}] {self.show}'

    def end_sale(self):
        success, message = self.seller.end_sale(self.show)

        if not success:
            return success, message

        self.status = self.SALE_ENDED
        self.save()

        tickets = message.get('tickets')
        sold_status = ['vendu', 'sold']

        # Change ticket status if sold
        for ticket in tickets:
            instance = Ticket.objects.filter(uuid=ticket['uuid']).first()
            if instance and ticket['status'] in sold_status:
                instance.sold = True
                instance.save()

        return success, message


