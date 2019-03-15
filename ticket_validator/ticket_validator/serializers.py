from rest_framework import serializers

from .models import Ticket


class TicketScanRequest(serializers.Serializer):
    uuid = serializers.UUIDField()


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'uuid',
            'show',
        )


class ReceiveTicketSerializer(serializers.Serializer):
    tickets = TicketSerializer(many=True)
