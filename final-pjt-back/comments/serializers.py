from rest_framework import serializers
# from django.contrib.auth import get_user_model
from .models import Review

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("like_users", "dislike_users", "created_at", "movie", "user",)