from django.urls import path
from apps.core.views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('', ReviewListCreateView.as_view()),
    path('<int:pk>/', ReviewDetailView.as_view()),
]