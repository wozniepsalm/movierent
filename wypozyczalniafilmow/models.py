from django.db import models


# Lista wyboru formatu filmów
MOVIE_FORMATS = (
    ('CD', 'Płyta CD'),
    ('W', 'Wersja cyfrowa'),
    ('VHS', 'Kaseta VHS'),
)
PLEC_WYBOR = (
    ('M', 'Mężczyzna'),
    ('K', 'Kobieta'),
    ('I', 'Inna'),
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


class ProductionYear(models.Model):
    """Model reprezentujący rok produkcji filmu."""
    year = models.PositiveSmallIntegerField(help_text="Rok produkcji filmu.")

    def __str__(self):
        return str(self.year)


class Movie(models.Model):
    """Model reprezentujący film w wypożyczalni."""
    title = models.CharField(max_length=100, help_text="Tytuł filmu.")
    production_year = models.ForeignKey(ProductionYear, null=True, blank=False, on_delete=models.SET_NULL, help_text="Rok produkcji filmu.")
    duration_minutes = models.PositiveIntegerField(help_text="Czas trwania filmu w minutach.")  
    movie_format = models.CharField(max_length=3, choices=MOVIE_FORMATS, default='W', help_text="Format filmu.")
    director = models.ForeignKey(Director, null=True, blank=False, on_delete=models.SET_NULL, help_text="Reżyser filmu.")
    genre = models.ForeignKey(Genre, null=True, blank=False, on_delete=models.SET_NULL, help_text="Gatunek filmowy.")
   
    def __str__(self):
        return self.title 
    
    def is_rented(self):
        """Sprawdza, czy film jest aktualnie wypożyczony."""
        active_rentals = self.rental_set.filter(return_date__isnull=True).first()
        return "Wypożyczony" if active_rentals else "Dostępny"
     

       

class Customer(models.Model):
    """Model reprezentujący klienta wypożyczalni i film który aktualnie wypożycza."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    plec = models.CharField(max_length=1, choices=PLEC_WYBOR, default='I', help_text="Płeć klienta.")
    data_dodania = models.DateTimeField(auto_now_add=True, help_text="Data i godzina dodania klienta do systemu.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 

    def is_renting(self):
        """Sprawdza, czy klient aktualnie wypożycza film."""
        active_rental = self.rental_set.filter(return_date__isnull=True).first()
        if active_rental:
            return active_rental.movie.title
        return "Brak wypożyczonych filmów"


class Rental(models.Model):
    """Model reprezentujący historię wypożyczeń filmów przez klientów."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, help_text="Klient wypożyczający film.")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, help_text="Wypożyczony film.")
    rental_date = models.DateTimeField(auto_now_add=True, help_text="Data i godzina wypożyczenia filmu.")
    return_date = models.DateTimeField(null=True, blank=True, help_text="Data i godzina zwrotu filmu.")

    def __str__(self):
        return f"{self.customer} wypożyczył {self.movie.title} dnia {self.rental_date}"

