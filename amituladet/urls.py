
from django.urls import path, include

urlpatterns = [
    path('api/', include('account.urls', namespace='account')),
    path('api/', include('song.urls', namespace='song')),
]
