from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import generics
from rest_framework.response import Response

from apps.email.choices import EmailType
from apps.email.generic import Email

from ..models import User
from ..serializers import reset_password


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = reset_password.ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = User.objects.filter(email=serializer.validated_data["email"], is_active=True).first()
        if not instance:
            return Response({}, status=200)

        instance.reset_password_code = get_random_string(length=64)
        instance.save(update_fields=("reset_password_code",))
        if request.GET.get("admin_portal"):
            password_verification_link = settings.PASSWORD_VERIFICATION_ADMIN_PORTAL_URL.format(
                reset_password_code=instance.reset_password_code
            )
        else:
            password_verification_link = settings.PASSWORD_VERIFICATION_URL.format(
                reset_password_code=instance.reset_password_code
            )

        Email([instance], EmailType.EMAIL_RESET_PASSWORD_SUBJECT, EmailType.EMAIL_RESET_PASSWORD_BODY).send(
            context_func=lambda user: {"password_verification_link": password_verification_link}
        )
        return Response({}, status=200)


class ResetPasswordVerifyView(generics.UpdateAPIView):
    serializer_class = reset_password.ResetPasswordVerifySerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = "reset_password_code"

    def perform_update(self, serializer):
        serializer.save(reset_password_code=None)
