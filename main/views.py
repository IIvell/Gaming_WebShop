from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from .models import Igrica, Kupac

## Create your views here.

def index(request, id):
    ls = Igrica.objects.get(id=id)
    return render (request, 'main/list.html', {'ls':ls})

def homepage(request):
    i = Igrica.objects.all()
    return render(request, 'main/home.html', {'i':i})
    # primjetiti korištenje HTML-a

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Get the authenticated user
        user = form.get_user()
        
        # Check if the user is a superuser (admin)
        if user.is_superuser:
            return redirect('/admin')
        
        # Otherwise, proceed with the default behavior
        return super().form_valid(form)