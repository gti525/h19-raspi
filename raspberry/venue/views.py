from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from rest_framework.parsers import JSONParser

from .models import Billet
from .serializer import BilletSerializer 

class BilletScanView(generics.ListCreateAPIView):
    #Billet.date = "2019-03-07T21:29:46.857Z"
    queryset = Billet.objects.all()
    serializer_class = BilletSerializer
    permission_classes = ()
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        #queryset = date = models.DateTimeField(auto_now=True)
        return Response({'received data': request.data})
    
class BilletNew(generics.ListCreateAPIView):
    queryset = Billet.objects.all()
    serializer_class = BilletSerializer
    permission_classes = ()