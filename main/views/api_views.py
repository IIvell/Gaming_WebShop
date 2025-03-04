from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from ..serializers import IgricaSerializer, UserSerializer
from ..models import Igrica
import requests


class IgricaListAPIView(APIView):
    def get(self, request):
        url = "https://api.igdb.com/v4/games/"
        headers = {
            "Client-ID": "m1omcez0w0d381ai3t4ph15psb9qdx",
            "Authorization": "vwlk7a56i826otz3pyttsar87ilcxh",
        }
        data = "fields id, name, rating, cover.image_id; sort rating desc;"
        response = requests.post(url, headers=headers, data=data)

        print(f"API Response Status Code: {response.status_code}")  # Status code
        if response.status_code == 200:
            print(f"API Response Data: {response.json()}")  # Ispisivanje podataka
            return Response(response.json())
        else:
            print(f"Failed to fetch data, Status code: {response.status_code}")
            return Response({"error": "Failed to retrieve data"}, status=response.status_code)


class IgricaViewSet(viewsets.ModelViewSet):
    queryset = Igrica.objects.all()
    serializer_class = IgricaSerializer


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
        return User.objects.filter(pk=pk).first()

    def get(self, request, pk):
        user = self.get_object(pk)
        return Response(UserSerializer(user).data if user else {"detail": "Not found."},
                        status=status.HTTP_404_NOT_FOUND if not user else status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        return Response(serializer.data if serializer.is_valid() and serializer.save() else serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"detail": "User deleted."}, status=status.HTTP_204_NO_CONTENT)