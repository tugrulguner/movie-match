from django.urls import path, include
from movie_match.api.endpoints import MovieMatch, TMDBResult
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'movie-match', MovieMatch, basename='movie-match')
router.register(r'tmdb-result', TMDBResult, basename='tmdb-result')
# router.register(r'tmdb-result', MovieMatch.as_view({'post': 'tmdb_return'}), basename='tmdb-result')

urlpatterns = [
    path('', include(router.urls)),
]
