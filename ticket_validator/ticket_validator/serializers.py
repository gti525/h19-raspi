from rest_framework import serializers

from .models import Ticket, ScanLog


class TicketScanRequest(serializers.Serializer):
    uuid = serializers.CharField()


class ScanLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScanLog
        fields = (
            'created',
            'ticket_uuid',
            'status',
            'mobile_user',
        )


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = (
            'uuid',
            'show',
            'scanned',
        )

    # def to_representation(self, obj):
    #     return obj.uuid


class ReceiveTicketSerializer(serializers.Serializer):
    tickets = TicketSerializer(many=True)

