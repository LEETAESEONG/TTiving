from django.urls import path
from . import views

urlpatterns = [
    path("<int:movie_pk>/", views.commentList),
    path("delete_put/<int:comment_pk>/", views.delete_put),
    path("likes/<int:comment_pk>/", views.likes),
    path("dislikes/<int:comment_pk>/", views.dislikes),
    path("likes_or_dislikes/<int:comment_pk>/", views.likes_or_dislikes),
]
