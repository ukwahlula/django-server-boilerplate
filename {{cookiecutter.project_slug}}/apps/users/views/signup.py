from django.contrib.auth import login
from rest_framework import generics
from rest_framework.response import Response

from ..models import User
from ..serializers import signup
from ..signals import email_verification, phone_verification


class SignUpSendEmailView(generics.GenericAPIView):
    serializer_class = signup.SignUpSendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email, is_active=False).first()
        if user:
            email_verification.send(sender=User, users=[user])
        return Response({})


class SignUpVerifyEmailView(generics.UpdateAPIView):
    serializer_class = signup.SignUpVerifyEmailSerializer
    queryset = User.objects.filter(is_active=False)

    def perform_update(self, serializer):
        serializer.save(is_email_verified=True)


class SignUpSendSmsView(generics.UpdateAPIView):
    serializer_class = signup.SignUpSendSmsSerializer
    queryset = User.objects.filter(is_active=False)

    def perform_update(self, serializer):
        instance = serializer.save()
        phone_verification.send(sender=User, users=[instance])


class SignUpVerifyPhoneView(generics.UpdateAPIView):
    serializer_class = signup.SignUpVerifyPhoneSerializer
    queryset = User.objects.filter(is_active=False)

    def perform_update(self, serializer):
        serializer.save(is_phone_verified=True)


class SignUpPasswordView(generics.UpdateAPIView):
    serializer_class = signup.SignUpPasswordSerializer
    queryset = User.objects.filter(is_active=False)


class SignUpProfileView(generics.UpdateAPIView):
    serializer_class = signup.SignUpProfileSerializer
    queryset = User.objects.filter(is_active=False)


class SignUpFinishView(generics.UpdateAPIView):
    serializer_class = signup.SignUpFinishSerializer
    queryset = User.objects.filter(is_active=False)

    def perform_update(self, serializer):
        instance = serializer.save(is_active=True, phone_verification_code=None, email_verification_code=None)
        login(self.request, instance)
