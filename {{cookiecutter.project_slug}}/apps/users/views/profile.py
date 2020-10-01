from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics

from apps.generic.permissions import IsAuthenticatedAndActive

from ..models import User
from ..serializers import profile
from ..signals import email_verification, phone_verification


class ProfileMixin:
    permission_classes = (IsAuthenticatedAndActive,)
    queryset = User.objects.filter(is_active=True)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), is_active=True, pk=self.request.user.pk)


class ProfileRetrieveView(ProfileMixin, generics.RetrieveAPIView):
    serializer_class = profile.ProfileRetrieveSerializer


class ProfileUpdateView(ProfileMixin, generics.UpdateAPIView):
    serializer_class = profile.ProfileUpdateSerializer


class ProfilePasswordView(ProfileMixin, generics.UpdateAPIView):
    serializer_class = profile.ProfilePasswordSerializer


class ProfileDestroyView(ProfileMixin, generics.DestroyAPIView):
    pass


class ProfileSendVerificationEmailView(ProfileMixin, generics.UpdateAPIView):
    serializer_class = profile.SendVerificationEmailSerializer

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.email = serializer.validated_data["email"]
        email_verification.send(sender=User, users=[instance])


class ProfileSendVerificationSmsView(ProfileMixin, generics.UpdateAPIView):
    serializer_class = profile.SendVerificationSmsSerializer

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.phone = serializer.validated_data["phone"]
        phone_verification.send(sender=User, users=[instance])


class VerifyEmailView(ProfileMixin, generics.UpdateAPIView):
    serializer_class = profile.VerifyEmailSerializer

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.is_email_verified = True
        instance.email_verification_code = None
        instance.save(update_fields=("is_email_verified", "email_verification_code"))


class VerifyPhoneView(ProfileMixin, generics.UpdateAPIView):
    serializer_class = profile.VerifyPhoneSerializer

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.is_phone_verified = True
        instance.phone_verification_code = None
        instance.save(update_fields=("is_phone_verified", "phone_verification_code"))
