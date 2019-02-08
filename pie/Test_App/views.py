from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import Tech
from .models import Ticket
from .serializer import TechSerializer
from .serializer import TicketSerializer
# Create your views here.


class AllTech(ListAPIView):

    queryset = Tech.objects.all()
    serializer_class = TechSerializer

    def post(self, request, format=None):
        serializer = TechSerializer(data=request.data)
        if serializer.is_valid():
            #print(Tech.name2 == serializer.data.__getattribute__("name2"))
            serializer.save()
            #'print(serializer.data.__getattribute__('name2'))'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechView(APIView):

    def get(self, request, pk, format=None):
        try:
            tech = Tech.objects.get(pk=pk)
            serializer = TechSerializer(tech)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        tech = Tech.objects.get(pk=pk)
        tech.delete()
        return Response(status=status.HTTP_200_OK)


class AllTicket(ListAPIView):

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def post(self, request, format=None):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketView(APIView):

    def get(self, request, pk, format=None):
        try:
            ticket = Ticket.objects.get(pk=pk)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        ticket = Ticket.objects.get(pk=pk)
        ticket.delete()
        return Response(status=status.HTTP_200_OK)
