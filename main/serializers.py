from rest_framework import serializers
from .models import Igrica
from django.contrib.auth.models import User

class IgricaSerializer(serializers.ModelSerializer):
    igrica_naslov = serializers.CharField(
        required=True, 
        max_length=200, 
        error_messages={
            'required': 'Naslov igre je obavezan.',
            'max_length': 'Naslov igre ne može imati više od 200 karaktera.'
        }
    )
    igrica_sadrzaj = serializers.CharField(
        required=True, 
        error_messages={
            'required': 'Sadržaj igre je obavezan.'
        }
    )
    igrica_vrijeme_objave = serializers.DateTimeField(
        required=True, 
        error_messages={
            'required': 'Datum i vreme objave su obavezni.',
            'invalid': 'Neispravan format datuma. Očekuje se ISO 8601 format (npr. "2023-01-21T14:30:00Z").'
        }
    )

    class Meta:
        model = Igrica
        fields = ['igrica_naslov', 'igrica_sadrzaj', 'igrica_vrijeme_objave']

    def validate_igrica_vrijeme_objave(self, value):
        from datetime import datetime
        if value.date() < datetime.now().date():
            raise serializers.ValidationError('Datum objave ne može biti u prošlosti.')
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
        read_only_fields = ['id']