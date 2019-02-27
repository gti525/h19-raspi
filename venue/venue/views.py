from django.contrib.auth.models import User

from rest_framework import generics

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

