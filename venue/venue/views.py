from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Show, Venue, Ticket, Seller, ShowPublication
from .serializer import ShowSerializer, VenueSerializer, TicketSerializer
from .serializer import ShowStatsSerializer


class ShowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class ShowListCreateView(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class VenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class TicketShowListView(generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        show_id = self.kwargs['show_id']
        return Ticket.objects.filter(show=show_id)


class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class ShowStatsView(APIView):

    @swagger_auto_schema(responses={200: ShowStatsSerializer()})
    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        tickets = show.ticket_set.all()

        sold = tickets.filter(sold=True)
        scanned = sold.filter(scanned=True)

        data = {
            'sold': sold.count(),
            'scanned': scanned.count(),
            'total': tickets.count(),
        }

        serializer = ShowStatsSerializer(data=data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowPublishView(APIView):

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        sellers = Seller.objects.all()
        show_tickets = show.get_tickets()

        tickets = list(self.chunks(
            show_tickets,
            show_tickets.count()//sellers.count(),
        ))

        messages = []
        status_code = status.HTTP_201_CREATED

        for i, seller in enumerate(sellers):
            publication = ShowPublication.objects.filter(
                show=show,
                seller=seller,
            )

            if publication.exists():
                messages.append(f'[{seller}] Show already published')
                status_code = status.HTTP_400_BAD_REQUEST
                continue

            success, message = seller.create_show(show, tickets[i])

            if not success:
                messages.append(
                    f'[{seller}] {message}'
                )
                status_code = status.HTTP_400_BAD_REQUEST
                continue

            messages.append(f'[{seller}] {message}')

        return Response({'messages': messages}, status=status_code)


class ShowEndSaleView(APIView):

    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)

        publications = ShowPublication.objects.filter(
            show=show,
            status=ShowPublication.ON_SALE,
        )

        messages = []
        status_code = status.HTTP_200_OK

        if not publications.exists():
            return Response({'messages': "Ce spectacle n'est pas publié"})

        for publication in publications:
            success, message = publication.end_sale()

            if success:
                messages.append(
                    f'[{publication.seller}] Vente terminée avec succès: {message}'
                )
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                messages.append(
                    f'[{publication.seller}] Erreur: {message}'
                )

        return Response({'messages': messages}, status=status_code)


class ShowSellerDeleteView(APIView):

    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        sellers = Seller.objects.filter(active=True)

        messages = []
        status_code = status.HTTP_200_OK

        for seller in sellers:
            success, message = seller.delete_show(show)

        return Response({'messages': messages}, status=status_code)











