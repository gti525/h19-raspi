import requests


class BaseSellerClient:
    API_URL = ''
    API_TOKEN = ''

    def __init__(self, url, token):
        self.API_URL = url
        self.API_TOKEN = token

    def create_show(self, show):
        return NotImplementedError

    def delete_show(self, show):
        return NotImplementedError

    def end_sale(self, show):
        return NotImplementedError


class Vente1Client(BaseSellerClient):
    API_URL = 'https://sitevente1-serveur.herokuapp.com/api/'
    API_TOKEN = '5c78135549469d2354cd1789'

    def get_headers(self):
        return {
            'adminKey': self.API_TOKEN,
        }

    def create_show(self, show):
        payload = {
            'uuid': str(show.uuid),
            'title': show.name,
            'artist': show.artist or 'TBA',
            'date': show.date.isoformat().split('+')[0],
            'description': show.description,
            'price': show.ticket_price,
            'venue': {
                'uuid': str(show.venue.uuid),
                'name': show.venue.name,
                'address': show.venue.address,
                'capacity': show.venue.capacity,
            },
            'tickets': [{
                'uuid': str(ticket.uuid),
            } for ticket in show.get_tickets()],
            'status': 'opened',
        }

        response = requests.post(
            self.API_URL + '/api/events',
            json=payload,
            headers=self.get_headers(),
        )

        if not response.status_code == 200:
            return False, response.json().get('message')

        return True, response.json().get('message')

    def delete_show(self, show):
        url = f'{self.API_URL}/events/{show.uuid}'

        response = requests.delete(
            url,
            headers=self.get_headers(),
        )

        if not response.status_code == 200:
            return False, response.json().get('message')

        return True, response.json().get('message')

    def end_sale(self, show):
        url = f'{self.API_URL}/api/events/{show.uuid}/endSale'

        response = requests.post(
            url,
            headers=self.get_headers(),
        )

        if not response.status_code == 200:
            return False, response.json().get('message')

        return True, response.json().get('message')


class Vente2Client(BaseSellerClient):

    def get_headers(self):
        return {}

    def create_show(self, show):
        payload = {

        }

        response = requests.post(
            self.API_URL,
            json=payload,
            headers=self.get_headers(),
        )

        if not response.status_code == 201:
            return False

        return response.json()


__all__ = [
    'Vente1Client',
    'Vente2Client',
]
