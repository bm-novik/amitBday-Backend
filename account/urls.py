# From Django
from django.urls import path, include

# From project
from rest_framework import routers

from account.views import LoginAPIView, RegisterAPIView, RsvpView, CheckTokenAPIView
from song.views import PermissionViewSet

app_name = 'account'
router = routers.DefaultRouter()
router.register(prefix='permission', viewset=PermissionViewSet, basename='permission')

urlpatterns = [
    path('', include('knox.urls')),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('rsvp', RsvpView.as_view(), name='login'),
    path('check_token', CheckTokenAPIView.as_view(), name='check_token'),
]

urlpatterns += router.urls
