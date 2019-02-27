from rest_framework import serializers

from .models import Ticket, Show, Venue


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'


class VenueSerializer(serializers.ModelSerializer):
    shows = ShowSerializer(many=True, read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class ShowTicketSerializer(ShowSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
