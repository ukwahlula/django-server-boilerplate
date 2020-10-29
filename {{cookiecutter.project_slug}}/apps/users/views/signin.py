from django.contrib.auth import login, logout
from rest_framework import generics, serializers
from rest_framework.response import Response

from ..models import User
from ..serializers import signin
from ..signals import phone_verification


class SignInView(generics.GenericAPIView):
    serializer_class = signin.SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.is_2fa_enabled:
            phone_verification.send(sender=User, users=[user])
        else:
            login(request, serializer.validated_data["user"])
        return Response({})


class SignIn2FAView(generics.GenericAPIView):
    serializer_class = signin.SignIn2FASerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.phone_verification_code_2fa = None
        user.save(update_fields=("phone_verification_code_2fa",))
        login(request, user)
        return Response({})


class SignOutView(generics.GenericAPIView):
    serializer_class = serializers.Serializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({})
