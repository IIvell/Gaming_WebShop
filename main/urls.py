from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from main.views import IgricaListView, IgricaDetailView, CustomLoginView, IgricaListAPIView, IgricaViewSet,UserListCreateView, UserDetailView, SearchGameView, index, homepage

app_name = 'main'
router = DefaultRouter()
router.register(r'igred', IgricaViewSet, basename='igrica')

urlpatterns = [
    path('<int:id>', index, name='index'),
    path('', homepage, name='homepage'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
    path('igre/', IgricaListView.as_view(), name='list'),
    path('igre/<int:pk>/', IgricaDetailView.as_view(), name='detail'),
    path('api/igre/', IgricaListAPIView.as_view(), name='api-igre'),
    path('', include(router.urls)),
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('search/', SearchGameView.as_view(), name='search_games'),  # Postavljanje URL-a za pretragu
]
