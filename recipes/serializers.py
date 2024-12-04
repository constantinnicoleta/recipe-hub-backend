from rest_framework import serializers
from .models import Recipe, Category, Comment, Like, Following


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model.
    Handles author details, ownership check, and validation of images.
    Includes fields for likes and comments counts.
    """
    author = serializers.ReadOnlyField(source='author.username')
    is_author = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        # Validates that the image size is below 2MB
        if not value:
            return value
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size larger than 2MB!")
        if value.image.height > 4096 or value.image.width > 4096:
            raise serializers.ValidationError(
             "Image dimensions exceed 4096x4096px!")
        return value

    def get_is_author(self, obj):
        # Checks if the current user is the author of the recipe
        request = self.context.get('request')
        return request.user == obj.author

    class Meta:
        model = Recipe
        fields = [
            'id', 'author', 'title', 'description', 'ingredients',
            'instructions', 'image', 'created_at', 'updated_at',
            'is_author', 'likes_count', 'comments_count',
        ]


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Includes fields for the category ID and name.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Handles author details, ownership checks, and associations with recipes.
    """
    author = serializers.ReadOnlyField(source='author.username')
    is_author = serializers.SerializerMethodField()

    def get_is_author(self, obj):
        # Checks if the current user is the author of the comment
        request = self.context.get('request')
        return request.user == obj.author

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'recipe', 'content', 'created_at', 'is_author',
        ]


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    Provides details about the user who liked a recipe
    and the associated recipe.
    """
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Like
        fields = ['id', 'author', 'post', 'created_at']


class FollowingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Following model.
    Manages unique relationships between followers and followed users.
    Includes validations to prevent duplicate follows.
    """
    author = serializers.ReadOnlyField(source='author.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    def create(self, validated_data):
        # Handles unique constraints for the follower-followed relationship
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': 'Possible duplicate follow'})

    class Meta:
        model = Following
        fields = ['id', 'author', 'followed', 'followed_name', 'created_at']
