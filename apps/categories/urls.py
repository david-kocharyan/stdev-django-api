from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetCategoryView.as_view(), name='get_categories'),
]
