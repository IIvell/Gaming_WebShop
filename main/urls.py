from django.urls import path
from main.views import CustomLoginView, IgricaListView
from django.contrib.auth import views as auth_views
from . import views
from .views import IgricaDetailView
from .views import IgricaListAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IgricaViewSet
from .views import UserListCreateView, UserDetailView

app_name = 'main'

router = DefaultRouter()
router.register(r'igred', IgricaViewSet, basename='igrica')

urlpatterns = [
    path('<int:id>', views.index, name='index'),
    path('', views.homepage, name='homepage'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('igre/', IgricaListView.as_view(), name='list'),
    path('igre/<int:pk>/', IgricaDetailView.as_view(), name='detail'),
    path('api/igre/', IgricaListAPIView.as_view(), name='api-igre'),
    path('', include(router.urls)),
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
