from django.urls import path
from . import views

urlpatterns = [
    path("", views.movieList),
    path("<int:movie_pk>/", views.movieDetail),
    path("genres/", views.genreList),
    path("likes/<int:movie_pk>/", views.likes),
    path("dislikes/<int:movie_pk>/", views.dislikes),
    path("likes_or_dislikes/<int:movie_pk>/", views.likes_or_dislikes),
    path("poster/", views.getGenrePoster),
    path("search/<keyword>/", views.search),
    path("normal_recommendation/", views.normal_recommendation),
    path("find_best_movie/", views.find_best_movie),
    path("get_locations/", views.get_locations),

]
