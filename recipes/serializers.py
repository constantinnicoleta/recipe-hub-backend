from rest_framework import serializers
from .models import Recipe, Category, Comment, Like, Follow


# RecipeSerializer: Handles Recipe model with owner details, ownership check,
# image validation, and read-only fields for likes and comments count.
class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size larger than 2MB!")
        if value.image.height > 4096 or value.image.width > 4096:
            raise serializers.ValidationError("Image dimensions exceed 4096x4096px!")
        return value

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner

    class Meta:
        model = Recipe
        fields = [
            'id', 'owner', 'title', 'content', 'image', 'created_at', 'updated_at',
            'is_owner', 'likes_count', 'comments_count',
        ]



# CategorySerializer: Minimal serializer for the Category model with only ID and name.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



# CommentSerializer: Handles Comment model with owner details, ownership check,
# and association with posts.
class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'post', 'content', 'created_at', 'updated_at', 'is_owner',
        ]



# LikeSerializer: Simplified serializer for Like model with owner and post details.
class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'owner', 'post', 'created_at']        



# FollowSerializer: Handles Follow model with owner details and validation for
# unique relationships between followers and followed users.
class FollowSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'Possible duplicate follow'})

    class Meta:
        model = Follow
        fields = ['id', 'owner', 'followed', 'followed_name', 'created_at']