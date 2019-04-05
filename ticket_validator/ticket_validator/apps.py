import requests

from django.apps import AppConfig
from django.conf import settings


class TicketValidatorConfig(AppConfig):
    name = 'ticket_validator'
    verbose_name = "Système de gestion de tickets"

    def ready(self):
        print('Fetch tickets...')
        from .models import Ticket

        try:
            response = requests.get(
                settings.VENUE_URL + 'validator/fetch',
                headers={
                    'Authorization': 'Token %s' % settings.VENUE_TOKEN,
                }
            )

            for ticket in response.json():
                Ticket.objects.get_or_create(
                    uuid=ticket['uuid'],
                    defaults={
                        'show': ticket['show']['uuid'],
                    }
                )

        except Exception:
            pass

        print('Done')
