from rest_framework import serializers

from .models import Ticket


class TicketScanRequest(serializers.Serializer):
    uuid = serializers.CharField()


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'uuid',
            'show',
        )

    def to_representation(self, obj):
        return obj.uuid


class ReceiveTicketSerializer(serializers.Serializer):
    tickets = TicketSerializer(many=True)
