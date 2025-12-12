from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie, Customer, Rental
from .serializers import MovieSerializer, CustomerSerializer, RentalSerializer

@api_view(['GET', 'POST'])
def movie_list(request):
    """wyświetla wszystkie filmy lub dodanie nowego filmu."""
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    """pobieranie aktualizowanie i usuwanie pojedyńczego filmu"""
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


@api_view(['GET', 'POST'])
def customer_list(request):
    """get- wyświetlanie wszystkich klientów, 
       post- dodanie nowego klienta"""
    if request.method == 'GET':
        queryset = Customer.objects.all()
        search_query = request.query_params.get('nazwisko', None) 
       #tutaj to nazwisko to nazwa parametru poprostu analogicznie do parametru name z zajec
        if search_query:
            queryset = queryset.filter(last_name__icontains=search_query)
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def customer_detail(request, pk):
    """get- wyświetla pojedyńczego, 
       delete- usuwa pojedyńczego"""
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    
    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


@api_view(['GET', 'POST'])
def rental_list(request):
    """get- wyświetla wszystkie wypożyczenia,
       post- dodaje nowe wypożyczenie"""
    if request.method == 'GET':
        rentals = Rental.objects.all()
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RentalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def rental_detail(request, pk):
    """get- wyświetla pojedyńcze wypożyczenie,
       delete- usuwa pojedyńcze wypożyczenie"""
    try:
        rental = Rental.objects.get(pk=pk)
    except Rental.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    
    if request.method == 'GET':
        serializer = RentalSerializer(rental)
        return Response(serializer.data)
     
    elif request.method == 'DELETE':
        rental.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.http import HttpResponse
import datetime

from .models import Genre, Director, ProductionYear, Movie, Customer, Rental
from .serializers import GenreSerializer, DirectorSerializer, ProductionYearSerializer, MovieSerializer, CustomerSerializer, RentalSerializer



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
    permission_classes = [IsAuthenticatedOrReadOnly]

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





# Create your views here.
