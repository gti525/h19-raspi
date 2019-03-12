from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Show, Venue, Ticket
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
