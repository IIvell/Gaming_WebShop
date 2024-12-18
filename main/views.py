from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from .models import Igrica, Kupac
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.views.generic import DetailView

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
    
class IgricaListView(ListView):
    model = Igrica
    template_name = 'main/list.html'
    context_object_name = 'igre'

    def get_queryset(self):
        queryset = super().get_queryset()
        name_query = self.request.GET.get('name', '')
        date_query = self.request.GET.get('date', '')
        order_query = self.request.GET.get('order', '')

        if name_query:
            queryset = queryset.filter(igrica_naslov__icontains=name_query)
        if date_query:
            queryset = queryset.annotate(date_only=TruncDate('igrica_vrijeme_objave')).filter(date_only=date_query)

        # Apply ordering
        if order_query == 'name_asc':
            queryset = queryset.order_by('igrica_naslov')
        elif order_query == 'name_desc':
            queryset = queryset.order_by('-igrica_naslov')
        elif order_query == 'date_asc':
            queryset = queryset.order_by('igrica_vrijeme_objave')
        elif order_query == 'date_desc':
            queryset = queryset.order_by('-igrica_vrijeme_objave')

        return queryset
    
class IgricaDetailView(DetailView):
    model = Igrica
    template_name = 'main/igrica_detail.html'
    context_object_name = 'igrica'    