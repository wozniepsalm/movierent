from rest_framework import serializers
from .models import Genre, Director, ProductionYear, Movie, Customer, Rental, PLEC_WYBOR, MOVIE_FORMATS
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User

CURRENT_YEAR = date.today().year

class MovieSerializer(serializers.ModelSerializer):
    """Serializer dla modelu Movie."""
    director_name = serializers.StringRelatedField(source='director', read_only=True)
    genre_name = serializers.StringRelatedField(source= 'genre', read_only=True)
    production_year = serializers.StringRelatedField(source='production_year', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_title(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Tytuł filmu musi zaczynać się wielką literą.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Czas trwania filmu musi być większy niż 0 minut.")
        return value


class DirectorSerializer(serializers.ModelSerializer):
    """Serializer dla modelu Director."""
    class Meta:
        model = Director
        fields = '__all__' 
        validators = [
            UniqueTogetherValidator(
                queryset=Director.objects.all(),
                fields=['first_name', 'last_name'],
            )
        ]
    
    def validate(self, data):
        """walidacja całego obiektu reżysera."""
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        country = data.get('country')

        if first_name and not (first_name[0].isupper() and first_name.isalpha()):
            raise serializers.ValidationError("Imię reżysera musi zaczynać się wielką literą i zawierać tylko litery.")
        if last_name and not (last_name[0].isupper() and last_name.isalpha()):
            raise serializers.ValidationError("Nazwisko reżysera musi zaczynać się wielką literą i zawierać tylko litery.")
        if country and (len(country) != 2 or not country.isupper()):
            raise serializers.ValidationError("Kod kraju musi składać się z dwóch wielkich liter.")
        return data 



class GenreSerializer(serializers.ModelSerializer):
    """Serializer dla modelu Genre."""
    popularity_rank = serializers.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(10)])
    class Meta:
        model = Genre
        fields = '__all__'

class ProductionYearSerializer(serializers.ModelSerializer):
    """Serializer dla modelu ProductionYear.""" 
    year = serializers.IntegerField(validators=[MinValueValidator(1888, message = "rok nie może być mniejszy niż 1888(pierwszy film)"), MaxValueValidator(CURRENT_YEAR, message = "rok nie może być większy niż bieżący rok")])
    class Meta:
        model = ProductionYear
        fields = ['id', 'year'] 

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer dla modelu Customer."""
    class Meta:
        model = Customer
        fields = '__all__'
    
    def validate_first_name(self, value):
        if not (value[0].isupper() and value.isalpha()):
            raise serializers.ValidationError("Imię powininno zawierać tylko litery i rozpoczynać się wielką literą.")
        return value
    def validate_last_name(self, value):
        if not (value[0].isupper() and value.isalpha()):
            raise serializers.ValidationError("Nazwisko powininno zawierać tylko litery i rozpoczynać się wielką literą.")
        return value 

class RentalSerializer(serializers.ModelSerializer):
    """Serializer dla modelu Rental."""
    class Meta:
        model = Rental
        fields = '__all__'
    
    def validate(self, data):
        """walidacja całego obiektu wypożyczenia."""
        return_date = data.get('return_date')
        if self.instance:
            rental_date = self.instance.rental_date
        else:
            rental_date = timezone.now() 

        if return_date and rental_date and return_date < rental_date:
            raise serializers.ValidationError("Data zwrotu nie może być wcześniejsza niż data wypożyczenia.")
        return data

class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer do zarejestrowania użytkownika."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user