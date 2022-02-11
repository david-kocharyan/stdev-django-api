from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'crud', viewset=views.PostView, basename="crud")

urlpatterns = [
    path("", include(router.urls)),
    path('get-by-user/<int:pk>/', views.GetPostsByUserIdView.as_view(), name='get_posts_by_user_id'),
]
