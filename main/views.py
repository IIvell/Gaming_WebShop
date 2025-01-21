from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from .models import Igrica, Kupac
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.views.generic import DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Igrica
from .serializers import IgricaSerializer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from .serializers import UserSerializer

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

class IgricaListAPIView(APIView):
    def get(self, request):
        igre = Igrica.objects.all()
        serializer = IgricaSerializer(igre, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IgricaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IgricaViewSet(viewsets.ModelViewSet):
    queryset = Igrica.objects.all()
    serializer_class = IgricaSerializer

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class UserListCreateView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'detail': 'User deleted.'}, status=status.HTTP_204_NO_CONTENT)