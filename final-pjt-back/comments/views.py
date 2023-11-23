from django.shortcuts import render, get_list_or_404, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
from .models import Review
from movies.models import Movie
from rest_framework import status


# Create your views here.
@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
def commentList(request, movie_pk):
    reviews = Review.objects.filter(movie=movie_pk)
    if request.method == "GET":
        serializer = CommentSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            movie = Movie.objects.get(pk=movie_pk)
            print('test', movie)
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE", "PUT"])
@permission_classes([IsAuthenticated])
def delete_put(request, comment_pk):
    comment = get_object_or_404(Review, pk=comment_pk)
    if comment.user == request.user:
        if request.method == 'DELETE':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def likes(request, comment_pk):
    comments = Review.objects.get(pk=comment_pk)
    data={}
    if comments.like_users.filter(pk=request.user.pk).exists():
        comments.like_users.remove(request.user)
        data = {'likes_or_dislikes':0}
    else:
        print(request.user)
        comments.like_users.add(request.user)
        if comments.dislike_users.filter(pk=request.user.pk).exists():
            comments.dislike_users.remove(request.user)
        data = {'likes_or_dislikes':1}
    like_count = len(comments.like_users.all())
    dislike_count = len(comments.dislike_users.all())
    data['like_count'] = like_count
    data['dislike_count'] = dislike_count
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def dislikes(request, comment_pk):
    comments = Review.objects.get(pk=comment_pk)
    data={}
    if comments.dislike_users.filter(pk=request.user.pk).exists():
        comments.dislike_users.remove(request.user)
        data = {'likes_or_dislikes':0}
    else:
        comments.dislike_users.add(request.user.pk)
        if comments.dislike_users.filter(pk=request.user.pk).exists():
            comments.like_users.remove(request.user)
        data = {'likes_or_dislikes':-1}
    like_count = len(comments.like_users.all())
    dislike_count = len(comments.dislike_users.all())
    data['like_count'] = like_count
    data['dislike_count'] = dislike_count

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def likes_or_dislikes(request, comment_pk):
    comment = Review.objects.get(pk=comment_pk)
    data = {}
    like_count = len(comment.like_users.all())
    dislike_count = len(comment.dislike_users.all())
    if comment.like_users.filter(pk = request.user.pk).exists():
        data = {"likes_or_dislikes" : 1, 'like_count':like_count, 'dislike_count':dislike_count}
    elif comment.dislike_users.filter(pk = request.user.pk).exists():
        data = {"likes_or_dislikes" : -1, 'like_count':like_count, 'dislike_count':dislike_count}
    else:
        data = {"likes_or_dislikes" : 0, 'like_count':like_count, 'dislike_count':dislike_count}
    return Response(data, status=status.HTTP_200_OK)