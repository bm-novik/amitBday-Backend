
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from account.serializers import LoginSerializer, UserDetailSerializer, RegisterSerializer


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    # Login API
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        }, status=status.HTTP_200_OK)


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    # Register API
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data={
            "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]},
            status=status.HTTP_201_CREATED)
