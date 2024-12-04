from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Count
from .models import Recipe, Category, Comment, Like, Following
from .serializers import (
    RecipeSerializer, CategorySerializer, CommentSerializer,
    LikeSerializer, FollowingSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth import authenticate, login, logout


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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

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
    if Like.objects.filter(user=user, recipe=recipe).exists():
        Like.objects.filter(user=user, recipe=recipe).delete()
        return Response({'message': 'Recipe unliked'}, status=status.HTTP_204_NO_CONTENT)
    else:
        Like.objects.create(user=user, recipe=recipe)
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

    follower = request.user    

    if Following.objects.filter(follower=follower, following=user_to_follow).exists():
        Following.objects.filter(follower=follower, following=user_to_follow).delete()
        return Response({'message': 'Unfollowed user'}, status=status.HTTP_204_NO_CONTENT)
    else:
        Following.objects.create(follower=follower, following=user_to_follow)
        return Response({'message': 'Followed user'}, status=status.HTTP_201_CREATED)


#Custom login view to authenticate the user and notify on success/failure.
class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(
                {"message": f"Welcome back, {user.username}!", "state": "logged_in"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials", "state": "logged_out"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


#Custom logout view to log out the user and notify on success.
class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"message": "You have been logged out successfully!", "state": "logged_out"},
            status=status.HTTP_200_OK,
        )


#View to check the user's current authentication state.
class UserStatusView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    "is_logged_in": True,
                    "user": {
                        "id": request.user.id,
                        "username": request.user.username,
                        "email": request.user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response({"is_logged_in": False}, status=status.HTTP_200_OK)        