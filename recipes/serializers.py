from django.contrib.auth.models import User 
from rest_framework import serializers
from .models import Recipe, Category, Comment, Like, Following


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Includes fields for the category ID and name.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model.
    Handles author details, ownership check,
    and includes fields for likes and comments counts.
    """
    author = serializers.ReadOnlyField(source='author.username')
    is_author = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_name = serializers.ReadOnlyField(source="category.name") 

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request.user == obj.author

    class Meta:
        model = Recipe
        fields = [
            'id', 'author', 'title', 'description', 'ingredients',
            'instructions', 'category', 'created_at', 'updated_at',
            'is_author', 'likes_count','category_name', 'comments_count',
        ]



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
    follower_name = serializers.ReadOnlyField(source='follower.username')
    following_name = serializers.ReadOnlyField(source='following.username')

    def create(self, validated_data):
        # Handles unique constraints for the follower-followed relationship
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': 'Possible duplicate follow'})

    class Meta:
        model = Following
        fields = ['id', 'follower', 'follower_name', 'following', 'following_name', 'created_at']


class FeedSerializer(serializers.Serializer):
    """
    Serializer to handle feed data, including recipes, likes, comments, and follows.
    """
    type = serializers.CharField()
    created_at = serializers.DateTimeField()
    data = serializers.JSONField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]    
