from django.urls import path
from apps.search.views import SearchListView

urlpatterns = [
    path('', SearchListView.as_view()),
]