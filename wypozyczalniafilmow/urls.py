from django.urls import path, include
from . import views

urlpatterns = [
    path('movies/', views.movie_list, name='movie-list'),
    path('movies/<int:pk>/', views.movie_detail),

    path('customers/', views.customer_list, name='customer-list'),
    path('customers/<int:pk>/', views.customer_detail),

    path('rentals/', views.rental_list, name='rental-list'),
    path('rentals/<int:pk>/', views.rental_detail),

    