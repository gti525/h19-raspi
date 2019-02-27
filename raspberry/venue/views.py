from django.contrib.auth.models import User

from rest_framework import generics

from .models import Billet
from .serializer import BilletSerializer 

class BilletScanView(generics.ListCreateAPIView):
    queryset = Billet.objects.all()
    serializer_class = BilletSerializer
    permission_classes = ()

