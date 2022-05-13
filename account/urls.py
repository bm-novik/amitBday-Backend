# From Django
from django.urls import path, include

# From project
from account.views import LoginAPIView, RegisterAPIView, RsvpView

app_name = 'account'
urlpatterns = [
    path('', include('knox.urls')),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('rsvp', RsvpView.as_view(), name='login'),
]

