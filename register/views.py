from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Ako je forma validna, sačuvaj novog korisnika
            user = form.save()
            
            # Automatically log in the user after registration
            login(request, user)
            
            # Preusmeri korisnika na početnu stranicu
            return redirect('/')  # Redirect to the home page
    else:
        form = RegisterForm()
    
    return render(request, 'register/register.html', {'form': form})
