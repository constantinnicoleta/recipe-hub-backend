from django.urls import path
from .views import (
    RecipeListCreateView, RecipeDetailView, CategoryListView,
    CategoryDetailView, 
    FeedView, follow_user, UserListView, check_follow_status,
)

urlpatterns = [
    path('feed/', FeedView.as_view(), name='user-feed'),
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/follow/', follow_user, name='follow-user'),
    path('users/<int:user_id>/is-following/', check_follow_status, name='check-follow-status'),
]
