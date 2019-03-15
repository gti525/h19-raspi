from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import TicketScanRequest, ReceiveTicketSerializer
from .models import Ticket, ScanLog


class TicketScanView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = TicketScanRequest(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.filter(
            uuid=serializer.validated_data['uuid']
        ).first()

        if not ticket:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if ticket.scanned:
            ScanLog.objects.create(
                ticket_uuid=ticket.uuid,
                status='FAIL'
            )
            return Response(status=status.HTTP_409_CONFLICT)

        ticket.scanned = True
        ticket.save()

        ScanLog.objects.create(
            ticket_uuid=ticket.uuid,
            status='OK',
        )

        return Response(status=status.HTTP_200_OK)


class ReceiveTicketView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        serializer = ReceiveTicketSerializer(
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        print(serializer.validated_data)
        print(serializer.validated_data['tickets'])

        for ticket in serializer.validated_data['tickets']:
            Ticket.objects.get_or_create(
                uuid=ticket['uuid'],
                show=ticket['show'],
            )

        return Response(status=status.HTTP_200_OK)
