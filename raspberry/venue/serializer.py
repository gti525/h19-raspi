from rest_framework import serializers

from .models import Billet

class BilletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billet
        fields = '__all__'
