from rest_framework import serializers
from .models import Tech
from .models import Ticket


class TechSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tech
        fields = ('id', 'short_name', 'name', 'name2')


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'
