from django.shortcuts import render, get_list_or_404, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Genre, MovieLocation
from .serializers import MovieSerializer, GenreSerializer, GenreLikeSerializer, MovieLocationSerializer
from rest_framework import status
from accounts.models import User
from comments.models import Review

@api_view(["GET"])
def movieList(request):
    if request.method == "GET":
        movies = get_list_or_404(Movie)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
@api_view(["GET"])
def movieDetail(request, movie_pk):
    if request.method == "GET":
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

@api_view(["GET"])
def genreList(request):
    if request.method == "GET":
        genres = get_list_or_404(Genre)
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def likes(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    data = {}
    if movie.like_users.filter(pk = request.user.pk).exists():
        movie.like_users.remove(request.user)
        data = {'likes_or_dislikes':0}
    else:
        movie.like_users.add(request.user)
        if movie.dislike_users.filter(pk = request.user.pk).exists():
            movie.dislike_users.remove(request.user)
        data = {'likes_or_dislikes':1}
    return Response(data, status= status.HTTP_200_OK)

@api_view(["POST"])
def dislikes(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    data = {}
    if movie.dislike_users.filter(pk = request.user.pk).exists():
        movie.dislike_users.remove(request.user)
        data = {'likes_or_dislikes':0}
    else:
        movie.dislike_users.add(request.user)
        if movie.dislike_users.filter(pk = request.user.pk).exists():
            movie.like_users.remove(request.user)
        data = {'likes_or_dislikes':-1}
    return Response(data, status= status.HTTP_200_OK)

@api_view(['GET'])
def likes_or_dislikes(request, movie_pk):
    print('testin2')
    movie = Movie.objects.get(pk=movie_pk)
    data = {}
    if movie.like_users.filter(pk = request.user.pk).exists():
        data = {"likes_or_dislikes" : 1}
    elif movie.dislike_users.filter(pk = request.user.pk).exists():
        data = {"likes_or_dislikes" : -1}
    else:
        data = {"likes_or_dislikes" : 0}
    return Response(data, status=status.HTTP_200_OK)

# 영화 포스터 가져오기
@api_view(["POST"])
def getGenrePoster(request):
    genre_id = request.data.get('id')
    genre = get_object_or_404(Genre, id=genre_id)
    movies = genre.movie_set.all()
    TMDB = "https://image.tmdb.org/t/p/w300"

    poster_paths = []
    for i in range(min(len(movies),4)):
        poster_paths.append(TMDB+movies[i].poster_path)
    return Response(poster_paths)

# 영화 검색 기능
@api_view(["GET"])
def search(request, keyword):
    movies = get_list_or_404(Movie)
    results = []
    for movie in movies:
        if keyword in movie.title:
            results.append(movie)
    serializer = MovieSerializer(results, many=True)
    return Response(serializer.data)

# 영화 추천 기능
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def normal_recommendation(request):
    user_pk = request.user.id
    person = get_object_or_404(User, pk=user_pk)
    like_genres = person.genre_likes.all()
    recommend_movies = Movie.objects.none()
    for like_genre in like_genres:
        movies = like_genre.movie_set.all()
        recommend_movies |= movies

    # 중복 제거
    recommend_movies = list(set(recommend_movies))

    # 정렬
    vote_avg_sort_movies = sorted(recommend_movies, key=lambda movie: movie.vote_average, reverse=True)
    release_date_sort_movies = sorted(recommend_movies, key=lambda movie: movie.release_date, reverse=True)
    title_sort_movies = sorted(recommend_movies, key=lambda movie: movie.title)

    VASM_serializer = MovieSerializer(vote_avg_sort_movies, many=True)
    RDSM_serializer = MovieSerializer(release_date_sort_movies, many=True)
    TSM_serializer = MovieSerializer(title_sort_movies, many=True)
    return Response((RDSM_serializer.data, VASM_serializer.data, TSM_serializer.data))

@api_view(["GET"])
def find_best_movie(request):
    # 영화를 전부 다 가져와서 비교
    movies = get_list_or_404(Movie)
    total_like_users = sum(len(movie.like_users.all()) for movie in movies)

    genres = get_list_or_404(Genre)
    print(Review)

    reviews = Review.objects.all()
    # 장르 순서 및 장르 별 점수 부여
    genres_rank = []
    genres_dict = {}
    max_genre_like_users = 0
    for genre in genres:
        if max_genre_like_users < len(genre.like_users.all()):
            max_genre_like_users = len(genre.like_users.all())
        genres_rank.append((genre.id, len(genre.like_users.all())))
    genres_rank.sort(key=lambda x: x[1], reverse=True)
    # score = 10
    # disCount = round(10/len(genres), 1)
    for gr in genres_rank:
        genres_dict[gr[0]] = round(gr[1]/max_genre_like_users, 1) if max_genre_like_users else 0
        # genres_dict[gr[0]] = score
        # score -= disCount

    max_like_users = max_comments_counts = 0
    # 유저가 매긴 점수
    results = []
    for movie in movies:
        movie_reviews = movie.review_set.all()
        if max_comments_counts < len(movie_reviews):
            max_comments_counts = len(movie_reviews)
        
        if max_like_users < len(movie.like_users.all()):
            max_like_users = len(movie.like_users.all())


    for movie in movies:
        max_genre_score = 0
        for genre in movie.genre_ids.all():
            if max_genre_score < genres_dict[genre.id]:
                max_genre_score = genres_dict[genre.id]
    
        # 외부참조로 영화에 해당하는 댓글을 가져온다.
        movie_reviews = movie.review_set.all()

        avg_rank = round(sum(review.rank for review in movie_reviews) / len(movie_reviews), 1) if movie_reviews else 0
        now_result = {
            "voteAverage": movie.vote_average,
            "likesCounts": round(len(movie.like_users.all())/max_like_users, 1) * 10 if max_like_users else 0,
            "rankAverage": avg_rank * 2,
            "reviewsCounts": round(len(movie_reviews)/max_comments_counts, 1) * 10 if max_comments_counts else 0,
            "genreRank": max_genre_score * 10,
        }
        now_result["getPoint"] = round(sum(now_result.values())/5, 1)
        now_result["totalPoint"] = sum(now_result.values())
        now_result["movie"] = MovieSerializer(movie).data
        results.append(now_result)
    results.sort(key=lambda x: x["totalPoint"], reverse=True)
    return Response(results[:10])


@api_view(['GET'])
def get_locations(request):
    movielocations = MovieLocation.objects.all()
    serializer = MovieLocationSerializer(movielocations, many=True)
    return Response(serializer.data)