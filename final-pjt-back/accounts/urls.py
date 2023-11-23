from django.urls import path
from . import views
urlpatterns = [
    path("userinfo/", views.userinfo),
    path('<int:user_pk>/follow/', views.follow),
    path("<int:user_pk>/picture/", views.picture),
    path("<int:user_pk>/profile/", views.profile),
    path("delete/", views.delete),
    path("<int:user_pk>/get_follow_status/", views.get_follow_status),
    path("<int:genre_pk>/pick_genre/", views.pickGenre),
    path("picked_genre/", views.pickedGenre),
]
