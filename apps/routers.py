from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.user.urls')),
    path('offers/', include('apps.rent.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('search/', include('apps.search.urls')),
    path('reviews/', include('apps.core.urls'))
]