from rest_framework import serializers
from .models import Genre, Director, ProductionYear, Movie, Customer, Rental, PLEC_WYBOR, MOVIE_FORMATS
from django.core.exeptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator


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

def multiple_of_two(value):
    if value % 2 != 0:
        raise serializers.ValidationError("Ocena popularności musi być wielokrotnością 2 (np. 0, 2, 4, 6, 8, 10).")

class GenreSerializer(serializers.ModelSerializer):
    """Serializer dla modelu Genre."""
    popularity_rank = serializers.IntegerField(validators= [multiple_of_two])
    class Meta:
        model = Genre
        fields = '__all__'

class ProductionYearSerializer(serializers.ModelSerializer):
    """Serializer dla modelu ProductionYear."""
    class Meta:
        model = ProductionYear
        fields = ['id', 'year']

