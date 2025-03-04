from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from ..models import Igrica


def index(request, id):
    igrica = get_object_or_404(Igrica, id=id)
    return render(request, 'main/list.html', {'igrica': igrica})


def homepage(request):
    igre = Igrica.objects.all()
    print(f"Games fetched from DB: {igre}")  # Ispisivanje svih igara s baze
    return render(request, 'main/home.html', {'igre': igre})


def custom_logout(request):
    logout(request)
    return redirect('homepage')