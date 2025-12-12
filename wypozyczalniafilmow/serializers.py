from rest_framework import serializers
from .models import Genre, Director, ProductionYear, Movie, Customer, Rental, PLEC_WYBOR, MOVIE_FORMATS
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator, MaxValueValidator, MinValueValidator
from datetime import date
from django.utils import timezone

CURRENT_YEAR = date.today().year

class MovieSerializer(serializers.Serializer): 
    """Serializer dla modelu Movie."""
   id = serializers.IntegerField(read_only=True)
   title = serializers.CharField(required=True, max_length=100)
   production_year = serializers.PrimaryKeyRelatedField(queryset=ProductionYear.objects.all())
   duration_minutes = serializers.IntegerField(required=True)
   movie_format = serializers.ChoiceField(choices=MOVIE_FORMATS, default='W')
   director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all())
   genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())  

    def create(self, validated_data): 
        return Movie.objects.create(**validated_data)  
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.production_year = validated_data.get('production_year', instance.production_year)
        instance.duration_minutes = validated_data.get('duration_minutes', instance.duration_minutes)
        instance.movie_format = validated_data.get('movie_format', instance.movie_format)
        instance.director = validated_data.get('director', instance.director)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.save()
        return instance 

    def validate_title(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Tytuł filmu powinen zaczynać się wielką literą.")
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
