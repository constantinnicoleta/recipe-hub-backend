from django.urls import path
from .views import (
    RecipeListCreateView, RecipeDetailView, CategoryListView,
    CommentListCreateView, CommentDetailView,CategoryDetailView, 
    CustomLoginView, CustomLogoutView, FeedView,
    UserStatusView, like_recipe, follow_user, UserListView,
    check_follow_status,
)

urlpatterns = [
    path('feed/', FeedView.as_view(), name='user-feed'),
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('recipes/<int:recipe_id>/like/', like_recipe, name='like-recipe'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/follow/', follow_user, name='follow-user'),
    path('users/<int:user_id>/is-following/', check_follow_status, name='check-follow-status'),
]
