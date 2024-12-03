from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Count
from .models import Recipe, Category, Comment, Like, Following
from .serializers import (
    RecipeSerializer, CategorySerializer, CommentSerializer,
    LikeSerializer, FollowingSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly


# RecipeListCreateView: Handles listing all recipes and creating a new recipe.
# Only authenticated users can create a recipe, but anyone can view them.
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# RecipeDetailView: Handles retrieving, updating, or deleting a single recipe by ID.
# Only the owner of the recipe or an authenticated user can update/delete.
class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


# CategoryListView: Handles listing all categories.
# Categories are read-only and visible to all users.
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# CommentListCreateView: Handles listing all comments and creating a new comment.
# Only authenticated users can comment, but anyone can view them.
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# CommentDetailView: Handles retrieving, updating, or deleting a single comment by ID.
# Only the owner of the comment or an authenticated user can update/delete.
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


# like_recipe: Function-based view for liking or unliking a recipe.
# If the user has already liked the recipe, the like is removed (unliked).
# If not, a like is added.
@api_view(['POST'])
def like_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if Like.objects.filter(author=user, post=recipe).exists():
        Like.objects.filter(author=user, post=recipe).delete()
        return Response({'message': 'Recipe unliked'}, status=status.HTTP_204_NO_CONTENT)
    else:
        Like.objects.create(author=user, post=recipe)
        return Response({'message': 'Recipe liked'}, status=status.HTTP_201_CREATED)


# follow_user: Function-based view for following or unfollowing another user.
# If the user is already following, the follow is removed (unfollowed).
# If not, a follow is created.
@api_view(['POST'])
def follow_user(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if Follow.objects.filter(author=request.user, followed=user_to_follow).exists():
        Follow.objects.filter(author=request.user, followed=user_to_follow).delete()
        return Response({'message': 'Unfollowed user'}, status=status.HTTP_204_NO_CONTENT)
    else:
        Follow.objects.create(author=request.user, followed=user_to_follow)
        return Response({'message': 'Followed user'}, status=status.HTTP_201_CREATED)