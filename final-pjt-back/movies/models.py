from django.db import models
from django.conf import settings


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="genre_likes")

class Movie(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()
    genre_ids = models.ManyToManyField(Genre)
    vote_average = models.FloatField()
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    poster_path = models.TextField()

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="movie_likes")
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="movie_dislikes")

class MovieLocation(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    POI_NM = models.CharField(max_length=100)
    CTPRVN_NM = models.CharField(max_length=100)
    SIGNGU_NM = models.CharField(max_length=100)
    LEGALDONG_NM = models.CharField(max_length=100)
    LI_NM = models.CharField(max_length=100, null=True)
    LNBR_NO = models.CharField(max_length=30, null=True)
    LC_LO = models.CharField(max_length=30)
    LC_LA = models.CharField(max_length=30)
