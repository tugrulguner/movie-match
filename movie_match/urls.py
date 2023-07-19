from django.urls import path, include
from movie_match.api.endpoints import MovieMatch
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'movie/suggestion', MovieMatch, basename='movie-match')

urlpatterns = [
    path('', include(router.urls)),
]
