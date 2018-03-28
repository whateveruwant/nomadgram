from rest_framework import serializers
from . import models
from nomadgram.images import serializers as images_serializers

class UserProfileSerializer(serializers.ModelSerializer):
    images = images_serializers.CountImageSerializer(many=True)
    post_count = serializers.ReadOnlyField() # 해당 필드들을 수정하지 않기위해
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'username',
            'name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
            'images'
        )


class ListUserSerailizer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name'
        )