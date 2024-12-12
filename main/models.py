from django.db import models
from django.contrib.auth.models import User

class Igrica(models.Model):
    igrica_naslov = models.CharField(max_length=100)
    igrica_sadrzaj = models.TextField()
    igrica_vrijeme_objave = models.DateTimeField('date published')

class Kupac(models.Model):
    kupac_ime = models.CharField(max_length=25)
    kupac_prezime = models.CharField(max_length=50)
    kupac_broj_mobitela = models.CharField(max_length=10)
    kupac_igrice = models.ManyToManyField(Igrica)

# Create your models here.
