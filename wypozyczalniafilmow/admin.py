from django.contrib import admin
from .models import Genre, Director, ProductionYear, Movie

admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(ProductionYear)
admin.site.register(Movie)
# Register your models here.
