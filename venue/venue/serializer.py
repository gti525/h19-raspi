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
    show = ShowSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketReturnSerializer(serializers.ModelSerializer):
    status = serializers.CharField()

    class Meta:
        model = Ticket
        fields = 'uuid'


class ShowTicketSerializer(ShowSerializer):
    tickets = TicketSerializer(many=True, read_only=True)


class ShowStatsSerializer(serializers.Serializer):
    sold = serializers.IntegerField()
    scanned = serializers.IntegerField()
    total = serializers.IntegerField()
