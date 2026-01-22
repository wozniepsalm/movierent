from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('', views.api_root, name='api-root'),

    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='api_token_auth'),

    path('movies/', views.MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/', views.MovieDetail.as_view(), name='movie-detail'),

    path('genres/', views.GenreList.as_view(), name='genre-list'),
    path('genres/<int:pk>/', views.GenreDetail.as_view(), name='genre-detail'),

    path('customers/', views.CustomerList.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'),

    path('rentals/', views.RentalList.as_view(), name='rental-list'),
    path('rentals/<int:pk>/', views.RentalDetail.as_view(), name='rental-detail'),
    
    path('rentals/active/', views.ActiveRentalsList.as_view(), name='active-rentals'),
    path('directors/<int:id>/movies/', views.DirectorMoviesList.as_view(), name='director-movies'),
    
    path('directors/', views.DirectorList.as_view(), name='director-list'),
    path('directors/<int:pk>/', views.DirectorDetail.as_view(), name='director-detail'),
]