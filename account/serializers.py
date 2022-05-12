from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password']

        write_only_fields = ['password']
        read_only_fields = ["id"]

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(username=validated_data['username'],
                                            password=make_password(validated_data['password']))
            return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ["id"]
