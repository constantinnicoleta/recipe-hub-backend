from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, Following, Category
from .serializers import RecipeSerializer, FollowingSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from .serializers import (
    RecipeSerializer, CategorySerializer,
    FollowingSerializer, UserSerializer,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
)
from .permissions import IsAuthorOrReadOnly


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
        Ensure the API returns the category name instead of just ID.
        """
        return Recipe.objects.select_related('category')


class CategoryListView(generics.ListAPIView):
    """
    List all recipe categories.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.prefetch_related('recipes')


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single category by ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class UserListView(ListAPIView):
    """
    Returns a list of all registered users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


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


class FeedView(APIView):
    """
    Get the user's feed with recipes from followed users.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            following_users = Following.objects.filter(follower=user).values_list('following', flat=True)

            if not following_users:
                return Response([], status=status.HTTP_200_OK)

            recipes = Recipe.objects.filter(author__in=following_users).order_by("-created_at")[:10]
            follows = Following.objects.filter(follower=user).order_by("-created_at")[:10]

            recipe_data = RecipeSerializer(recipes, many=True, context={'request': request}).data
            follow_data = FollowingSerializer(follows, many=True, context={'request': request}).data

            feed = []
            feed.extend([{"type": "recipe", "data": r} for r in recipe_data])
            feed.extend([{"type": "follow", "data": f} for f in follow_data])

            feed = sorted(feed, key=lambda x: x["data"].get("created_at", ""), reverse=True)[:20]

            return Response(feed, status=status.HTTP_200_OK)

        except Exception as e:
            print("ERROR in FeedView:", str(e))
            return Response(
                {"error": "Something went wrong in the feed.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
