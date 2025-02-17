from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db.models import Count
from .models import Recipe, Category, Comment, Like, Following
from .serializers import (
    RecipeSerializer, CategorySerializer, CommentSerializer,
    LikeSerializer, FollowingSerializer
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
)
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth import authenticate, login, logout


class RecipeListCreateView(generics.ListCreateAPIView):
    """
    List all recipes or create a new one.
    Authenticated users can create; all users can view.
    """
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        If an `author` parameter is provided, filter recipes by author.
        Otherwise, return all recipes.
        """
        queryset = Recipe.objects.all()
        author = self.request.query_params.get('author')

        if author:
            queryset = queryset.filter(author__username=author)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a recipe by ID.
    Restricted to the author for edits; read-only for others.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_context(self):
        """
        Ensures `request` is passed into the serializer,
        so `is_author` is correctly calculated in the response.
        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Ensure the API returns the category name instead of just ID
        """
        return Recipe.objects.select_related('category')    


class CategoryListView(generics.ListAPIView):
    """
    List all recipe categories.
    Categories are read-only and visible to all users.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    """
    List all comments or create a new one.
    Authenticated users can comment; all users can view.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a comment by ID.
    Restricted to the author for edits; read-only for others.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['POST'])
def like_recipe(request, recipe_id):
    """
    Like or unlike a recipe.
    Toggles the like status for the authenticated user.
    """
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return Response(
            {'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if Like.objects.filter(user=user, recipe=recipe).exists():
        Like.objects.filter(user=user, recipe=recipe).delete()
        return Response(
            {'message': 'Recipe unliked'}, status=status.HTTP_204_NO_CONTENT)
    else:
        Like.objects.create(user=user, recipe=recipe)
        return Response(
            {'message': 'Recipe liked'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def follow_user(request, user_id):
    """
    Follow or unfollow a user.
    Toggles the follow status for the authenticated user.
    """
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    follower = request.user

    if Following.objects.filter(
        follower=follower,
        following=user_to_follow
    ).exists():
        # Unfollow the user if already followed
        Following.objects.filter(
            follower=follower,
            following=user_to_follow
        ).delete()
        return Response(
            {'message': 'Unfollowed user'}, 
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        # Follow the user if not already followed
        Following.objects.create(
            follower=follower,
            following=user_to_follow
        )
        return Response(
            {'message': 'Followed user'}, 
            status=status.HTTP_201_CREATED
        )


class CustomLoginView(APIView):
    """
    Custom login functionality.
    Authenticates a user and returns a success message or error.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response(
                {
                    "message": f"Welcome back, {user.username}!",
                    "state": "logged_in"
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "error": "Invalid credentials",
                "state": "logged_out"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class CustomLogoutView(APIView):
    """
    Custom logout functionality.
    Logs out a user and returns a success message.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"message": "You have been logged out successfully!",
             "state": "logged_out"},
            status=status.HTTP_200_OK,
        )


class UserStatusView(APIView):
    """
    Check the user's current authentication status.
    Provides user details if authenticated.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "is_logged_in": True,
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email
                },
            }, status=200)
        return Response({"is_logged_in": False}, status=200)
