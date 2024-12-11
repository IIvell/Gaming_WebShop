from django.urls import path
from main.views import CustomLoginView
from django.contrib.auth import views as auth_views
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.homepage, name='homepage'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]