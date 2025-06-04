from django.urls import path
from apps.bookings.views import (
    BookingListCreateView,
    BookingStatusView,
    BookingCancelView
)
urlpatterns = [
    path('', BookingListCreateView.as_view()),
    path('<int:pk>/status/', BookingStatusView.as_view()),
    path('<int:pk>/cancel/', BookingCancelView.as_view()),

]