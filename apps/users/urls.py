from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('sign-up/', views.UserRegisterView.as_view(), name='sign_up'),
    path('sign-in/', views.TokenObtainPairPatchedView.as_view(), name='sign_in'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('logout-all/', views.UserLogoutAllView.as_view(), name='logout_all'),
    path('me/', views.CurrentUserView.as_view(), name='me'),
    path('<int:pk>/', views.GetUserByIdView.as_view(), name='get_user_by_id'),
]
