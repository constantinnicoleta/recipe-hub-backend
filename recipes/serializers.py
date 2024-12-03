from rest_framework import serializers
from .models import Recipe, Category, Comment, Like, Following


# RecipeSerializer: Handles Recipe model with owner details, ownership check,
# image validation, and read-only fields for likes and comments count.
class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_author = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size larger than 2MB!")
        if value.image.height > 4096 or value.image.width > 4096:
            raise serializers.ValidationError("Image dimensions exceed 4096x4096px!")
        return value

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request.user == obj.author

    class Meta:
        model = Recipe
        fields = [
            'id', 'author', 'title', 'description', 'ingredients', 'instructions', 'image',
            'created_at', 'updated_at', 'is_author', 'likes_count', 'comments_count',
        ]



# CategorySerializer: Minimal serializer for the Category model with only ID and name.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



# CommentSerializer: Handles Comment model with owner details, ownership check,
# and association with posts.
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_author = serializers.SerializerMethodField()

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request.user == obj.author

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'post', 'content', 'created_at', 'updated_at', 'is_author',
        ]



# LikeSerializer: Simplified serializer for Like model with owner and post details.
class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Like
        fields = ['id', 'author', 'post', 'created_at']        



# FollowingSerializer: Handles Following model with owner details and validation for
# unique relationships between followers and followed users.
class FollowingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'Possible duplicate follow'})

    class Meta:
        model = Following
        fields = ['id', 'author', 'followed', 'followed_name', 'created_at']