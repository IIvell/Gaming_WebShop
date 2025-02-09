from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Igrica(models.Model):
    igrica_naslov = models.CharField(max_length=255)
    igrica_sadrzaj = models.TextField()
    igrica_vrijeme_objave = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(default=0)  # Sum of all ratings
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.igrica_naslov

    def average_rating(self):
        if self.review_count > 0:
            return self.rating / self.review_count
        return 0  # Default value if there are no reviews


class Review(models.Model):
    igrica = models.ForeignKey(Igrica, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link the review to a user
    review_text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.igrica.igrica_naslov}"


class Kupac(models.Model):
    kupac_ime = models.CharField(max_length=25)
    kupac_prezime = models.CharField(max_length=50)
    kupac_broj_mobitela = models.CharField(max_length=10)
    kupac_igrice = models.ManyToManyField(Igrica)

    def __str__(self):
        return self.kupac_ime


