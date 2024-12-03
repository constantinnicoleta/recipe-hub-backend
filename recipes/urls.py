from django.urls import path
from .views import (
    RecipeListCreateView, RecipeDetailView, CategoryListView,
    CommentListCreateView, CommentDetailView, like_recipe, follow_user
)

urlpatterns = [
    # Recipes
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),

    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # Comments
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

    # Likes
    path('recipes/<int:recipe_id>/like/', like_recipe, name='like-recipe'),

    # Follows
    path('users/<int:user_id>/follow/', follow_user, name='follow-user'),
]
