from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import Genre, Director, ProductionYear, Movie, Customer, Rental
from django.contrib.auth.models import User
from .serializers import GenreSerializer, DirectorSerializer, ProductionYearSerializer, MovieSerializer, CustomerSerializer, RentalSerializer, UserRegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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



class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUser]


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



def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html>
            <head><title>Wypożyczalnia</title></head>
            <body>
                <h1>Witaj w MovieRent!</h1>
                <p>Aktualna data serwera: {now}</p>
            </body>
        </html>
    """
    return HttpResponse(html)

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny] 

class CustomAuthToken(ObtainAuthToken):
    """ tak żeby widok logowania byl w przegladarce """
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Użyj formularza poniżej, aby się zalogować i uzyskać token.'})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })



# Create your views here.
