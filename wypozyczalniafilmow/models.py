from django.db import models


# Lista wyboru formatu filmów
MOVIE_FORMATS = (
    ('CD', 'Płyta CD'),
    ('W', 'Wersja cyfrowa'),
    ('VHS', 'Kaseta VHS'),
)


class Genre(models.Model):
    """Model reprezentujący gatunek filmowy."""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, help_text="Krótki opis gatunku filmowy.")
    typical_themes = models.CharField(
        max_length=200,
        blank=True,
        help_text="Typowe motywy i tematy występujące w tym gatunku."
    )
    is_documentary = models.BooleanField(default=True, help_text="Czy gatunek jest dokumentalny?")
    popularity_rank = models.PositiveSmallIntegerField(
        default=0,
        help_text="Ocena popularności (0–10) według oglądaczy."
    )

    def __str__(self):
        return self.name


class Director(models.Model):
    """Model reprezentujący reżysera filmu."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=2, help_text="Kod kraju, np. PL, US, GB")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    """Model reprezentujący film w wypożyczalni."""
    title = models.CharField(max_length=100)
    release_year = models.PositiveSmallIntegerField(help_text="Rok premiery filmu.")
    duration_minutes = models.PositiveIntegerField(help_text="Czas trwania filmu w minutach.")  
    movie_format = models.CharField(max_length=3, choices=MOVIE_FORMATS, default='W')
    director = models.ForeignKey(Director, null=True, blank=False, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

# Create your models here.
