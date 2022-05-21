from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from account.models import Rsvp
from account.serializers import LoginSerializer, UserSerializer, RsvpSerializer


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    # Login API
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'username': request.data.get('username', request.data.get('password')),
                                               'password': request.data.get('password')})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        }, status=status.HTTP_200_OK)


class RegisterAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'username': request.data.get('username', request.data.get('password')),
                                               'password': request.data.get('password'),
                                               'confirm_password': request.data.get('confirm_password', request.data.get('password')),
                                               'first_name': request.data.get('first_name'),
                                               'last_name': request.data.get('last_name'),
        }, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data={
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]},
            status=status.HTTP_201_CREATED)


class CheckTokenAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User.objects.all(), pk=request.user.pk)
        return Response(data={"user": self.get_serializer(user).data}, status=status.HTTP_200_OK)


class RsvpView(GenericAPIView):
    serializer_class = RsvpSerializer
    queryset = Rsvp.objects.all()

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(Rsvp.objects.all(), many=True).data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rsvp = serializer.save()
        return Response(RsvpSerializer(rsvp, context=self.get_serializer_context()).data,
                        status=status.HTTP_201_CREATED)
