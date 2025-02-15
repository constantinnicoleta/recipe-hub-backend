from django.urls import path
from .views import (
    RecipeListCreateView, RecipeDetailView, CategoryListView,
    CommentListCreateView, CommentDetailView,CustomLoginView, CustomLogoutView,
    UserStatusView, like_recipe, follow_user
)

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('recipes/<int:recipe_id>/like/', like_recipe, name='like-recipe'),
    path('users/<int:user_id>/follow/', follow_user, name='follow-user'),
]
