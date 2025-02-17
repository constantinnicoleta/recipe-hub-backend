from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from recipes.views import CustomLoginView, CustomLogoutView, UserStatusView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipes.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/token/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/custom-login/', CustomLoginView.as_view(), name='custom-login'),
    path('auth/custom-logout/', CustomLogoutView.as_view(), name='custom-logout'),
    path('auth/user-status/', UserStatusView.as_view(), name='user-status'),    
]