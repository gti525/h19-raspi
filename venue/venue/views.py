from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Show, Venue, Ticket
from .serializer import ShowSerializer, VenueSerializer, TicketSerializer


class ShowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = ()


class ShowListCreateView(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = ()


class VenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = ()


class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = ()


class TicketShowListView(generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        show_id = self.kwargs['show_id']
        return Ticket.objects.filter(show=show_id)


class ShowStatsView(APIView):

    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        tickets = show.tickets.all()

        sold = tickets.filter(sold=True)
        scanned = sold.filter(scanned=True)

        return Response({
            'show': show.id,
            'sold': sold.count(),
            'scanned': scanned.count(),
            'total': tickets.count(),
        })
