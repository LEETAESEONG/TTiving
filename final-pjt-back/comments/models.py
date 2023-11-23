from django.db import models
from django.conf import settings

# Create your models here.
class Review(models.Model):
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    rank = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='review_likes')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='review_dislikes')
