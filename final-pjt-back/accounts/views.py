from django.shortcuts import get_list_or_404, get_object_or_404

# rest_framework
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# models
from .models import User
from movies.models import Movie, Genre
from comments.models import Review

# serializers
from .serializers import UserSerializer, UserNameSerializer, UserFollowSerializer
from movies.serializers import MovieSerializer, GenreSerializer, GenreLikeSerializer
from comments.serializers import CommentSerializer

# Create your views here.


@api_view(["GET"])
def userinfo(request):
    if request.method == "GET":
        user = get_list_or_404(User)
        serializer = UserNameSerializer(user, many=True)
        user_Serializer = UserSerializer(user, many=True)
        return Response({'username':serializer.data, 'user':user_Serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    if request.method == "POST":
        person = get_object_or_404(User, pk=user_pk)
        data = {}
        if request.user in person.followers.all():
            person.followers.remove(request.user)
            data['status'] = 0
        else:
            person.followers.add(request.user)
            data["status"] = 1
        followings = person.followings.values()
        followers = person.followers.values()
        data['followings'] = followings
        data['followers'] = followers
        print(data)
        return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_follow_status(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)
    followings = UserSerializer(person.followings.all(), many=True)
    followers = UserSerializer(person.followers.all(), many=True)
    data = {'followings': followings.data, 'followers': followers.data}
    if request.user in person.followers.all():
        data['status'] = 1
    else:
        data['status'] = 0
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def picture(request, user_pk):
    if request.method == "POST":
        person = get_object_or_404(User, pk=user_pk)
        person.picture = request.data["picture"]
        person.save()
        serializer = UserSerializer(person)
        return Response(serializer.data)


@api_view(["GET"])
def profile(request, user_pk):
    person = User.objects.get(pk=user_pk)
    serializer = UserSerializer(person)
    like_movies = person.movie_likes.all()
    like_movie_serializers = MovieSerializer(like_movies, many=True)
    dislike_movies = person.movie_dislikes.all()
    dislike_movie_serializers = MovieSerializer(dislike_movies, many=True)
    comments = Review.objects.filter(user=person).order_by('-pk')
    comment_serializers = CommentSerializer(comments, many=True)

    return Response({"person": serializer.data, "like_movies": like_movie_serializers.data, "dislike_movies": dislike_movie_serializers.data, "comments": comment_serializers.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pickGenre(request, genre_pk):
    user_pk = request.user.id
    person = get_object_or_404(User, pk=user_pk)
    genre = get_object_or_404(Genre, pk=genre_pk)
    if genre in person.genre_likes.all():
        person.genre_likes.remove(genre)
    else:
        person.genre_likes.add(genre)
    serializer = UserSerializer(person)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pickedGenre(request):
    user_pk = request.user.id
    person = get_object_or_404(User, pk=user_pk)
    like_genres = person.genre_likes.all()

    serializers = GenreLikeSerializer(like_genres, many=True)
    return Response(serializers.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete(request):
    user = User.objects.get(id=request.user.id)
    if user:
        user.delete()
        return Response({"message": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)
    return Response({"message": "이미 탈퇴한 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)