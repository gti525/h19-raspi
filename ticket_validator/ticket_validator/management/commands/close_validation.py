import requests

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ticket_validator.models import Ticket
from ticket_validator.serializers import TicketSerializer


class Command(BaseCommand):
    help = 'Send ticket informations to Gestionnaire de salle'

    def handle(self, *args, **options):
        self.stdout.write('Querying tickets')
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)

        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]

        tickets_list = list(chunks(serializer.data, 20))

        for ticket_chunk in tickets_list:

            try:
                response = requests.post(
                    settings.VENUE_URL + 'validator/result',
                    headers={
                        'Authorization': 'Token %s' % settings.VENUE_TOKEN,
                    },
                    json=ticket_chunk,
                )

                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS('Success'))

                else:
                    print(response)
                    print(response.content)
                    self.stdout.write(self.style.ERROR('FAILED'))

            except requests.exceptions.RequestException as e:
                raise CommandError(e)


