from rest_framework import serializers
from .models import Movie, Genre, MovieLocation

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class GenreLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id",)

class MovieLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLocation
        fields = "__all__"