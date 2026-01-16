from rest_framework import generics, filters, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import Genre, Director, ProductionYear, Movie, Customer, Rental
from django.contrib.auth.models import User
from .serializers import GenreSerializer, DirectorSerializer, ProductionYearSerializer, MovieSerializer, CustomerSerializer, RentalSerializer, UserRegisterSerializer

class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DirectorList(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['last_name']

class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductionYearList(generics.ListCreateAPIView):
    queryset = ProductionYear.objects.all()
    serializer_class = ProductionYearSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductionYearDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductionYear.objects.all()
    serializer_class = ProductionYearSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    - zalogowani users (pracownicy) mogą oglądać (GET)
    - tylko admin może edytować lub usuwać (PUT, DELETE)
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff



class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['last_name']

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class RentalList(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

class RentalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]



class ActiveRentalsList(generics.ListAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rental.objects.filter(return_date__isnull=True)

class DirectorMoviesList(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        director_id = self.kwargs['id']
        return Movie.objects.filter(director__id=director_id)




class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny] 




# Create your views here.
