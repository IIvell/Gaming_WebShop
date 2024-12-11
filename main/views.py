from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

## Create your views here.

def index(request):
    return render (request, 'main/base.html', {})

def homepage(request):
    return render(request, 'main/home.html', {})
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