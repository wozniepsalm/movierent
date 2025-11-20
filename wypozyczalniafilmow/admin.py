from django.contrib import admin
from .models import Genre, Director, ProductionYear, Movie, Customer, Rental

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'typical_themes', 'is_documentary', 'popularity_rank')
    search_fields = ('name', 'typical_themes')
admin.site.register(Genre, GenreAdmin)

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'country')
    list_filter = ('country',)
    search_fields = ('first_name', 'last_name', 'country')
admin.site.register(Director, DirectorAdmin)

class ProductionYearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)
admin.site.register(ProductionYear, ProductionYearAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'production_year', 'duration_minutes', 'movie_format', 'director', 'genre', 'is_rented')
    list_filter = ('movie_format', 'production_year', 'director', 'genre')
    search_fields = ('title', 'director__first_name', 'director__last_name', 'genre__name')
admin.site.register(Movie, MovieAdmin)
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'plec', 'is_renting', 'data_dodania')
    readonly_fields = ('data_dodania',)
    list_filter = ('plec',)
    search_fields = ('first_name', 'last_name')
admin.site.register(Customer, CustomerAdmin) 

class RentalAdmin(admin.ModelAdmin):
    list_display = ('customer', 'movie', 'rental_date', 'return_date')
    list_filter = ('rental_date', 'return_date')
    search_fields = ('customer__first_name', 'customer__last_name', 'movie__title')
    readonly_fields = ('rental_date',)
admin.site.register(Rental, RentalAdmin)