from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # () 괄호 실수 주의
        model = get_user_model()
        fields = ("id", "username", "picture",)

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", )

class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("followings", )
