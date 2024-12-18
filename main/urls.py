from django.urls import path
from main.views import CustomLoginView, IgricaListView
from django.contrib.auth import views as auth_views
from . import views
from .views import IgricaDetailView

app_name = 'main'

urlpatterns = [
    path('<int:id>', views.index, name='index'),
    path('', views.homepage, name='homepage'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('igre/', IgricaListView.as_view(), name='list'),
    path('igre/<int:pk>/', IgricaDetailView.as_view(), name='detail'), 
]
