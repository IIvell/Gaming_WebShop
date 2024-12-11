from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Ako je forma validna, sačuvaj novog korisnika
            form.save()
            return redirect('/')  # Preusmeri korisnika na početnu stranicu
    else:
        form = RegisterForm()
    
    return render(request, 'register/register.html', {'form': form})
