from apps.generic.choices import BaseChoices


class SmsType(BaseChoices):
    PHONE_VERIFICATION = "PHONE_VERIFICATION"
    PHONE_VERIFICATION_2FA = "PHONE_VERIFICATION_2FA"
