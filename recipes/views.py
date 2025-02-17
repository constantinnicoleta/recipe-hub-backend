from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db.models import Count
from .models import Recipe, Category, Comment, Like, Following
from .serializers import (
    RecipeSerializer, CategorySerializer, CommentSerializer,
    LikeSerializer, FollowingSerializer, UserSerializer,
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
        Fetch either all recipes, recipes by author, or recipes filtered by category.
        """
        queryset = Recipe.objects.select_related('category')
        user = self.request.user
        author = self.request.query_params.get('author')
        category_id = self.request.query_params.get('category') 

        if author:
            queryset = queryset.filter(author__username=author)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if "my_recipes" in self.request.path and user.is_authenticated:
            return queryset.filter(author=user)

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
    List all recipe categories, ensuring all users' recipes appear.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Ensure all recipes appear in Categories, not just the logged-in user's.
        """
        return Category.objects.prefetch_related('recipes')


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single category by ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]    


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


class UserListView(ListAPIView):
    """
    Returns a list of all registered users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


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
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow or unfollow a user.
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    follower = request.user

    if Following.objects.filter(follower=follower, following=user_to_follow).exists():
        Following.objects.filter(follower=follower, following=user_to_follow).delete()
        return Response({'message': 'Unfollowed user'}, status=status.HTTP_204_NO_CONTENT)
    else:
        Following.objects.create(follower=follower, following=user_to_follow)
        return Response({'message': 'Followed user'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_follow_status(request, user_id):
    """
    Check if the logged-in user follows another user.
    """
    try:
        user_to_check = User.objects.get(id=user_id)
        is_following = Following.objects.filter(follower=request.user, following=user_to_check).exists()
        return Response({'is_following': is_following}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomLoginView(APIView):
    """
    Custom login functionality.
    Authenticates a user and returns a success message or error.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

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
    

import traceback 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Recipe, Like, Comment, Following
from .serializers import RecipeSerializer, LikeSerializer, CommentSerializer, FollowingSerializer

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            following_users = Following.objects.filter(follower=user).values_list('following', flat=True)

            if not following_users:
                return Response([], status=status.HTTP_200_OK)

            recipes = Recipe.objects.filter(author__in=following_users).order_by("-created_at")[:10]
            likes = Like.objects.filter(user__in=following_users).order_by("-created_at")[:10]
            comments = Comment.objects.filter(author__in=following_users).order_by("-created_at")[:10]
            follows = Following.objects.filter(follower=user).order_by("-created_at")[:10]

            recipe_data = RecipeSerializer(recipes, many=True, context={'request': request}).data
            like_data = LikeSerializer(likes, many=True, context={'request': request}).data
            comment_data = CommentSerializer(comments, many=True, context={'request': request}).data
            follow_data = FollowingSerializer(follows, many=True, context={'request': request}).data

            feed = []
            feed.extend([{"type": "recipe", "data": r} for r in recipe_data])
            feed.extend([{"type": "like", "data": l} for l in like_data])
            feed.extend([{"type": "comment", "data": c} for c in comment_data])
            feed.extend([{"type": "follow", "data": f} for f in follow_data])

            feed = sorted(feed, key=lambda x: x["data"].get("created_at", ""), reverse=True)[:20]

            return Response(feed, status=status.HTTP_200_OK)

        except Exception as e:
            print("🚨 ERROR in FeedView:", str(e))
            return Response({"error": "Something went wrong in the feed.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)