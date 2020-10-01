# flake8: noqa
# fmt: off
from .choices import ContentType

CONTENT_PRESETS= {
    # Emails
    ContentType.EMAIL_VERIFICATION_SUBJECT: {
        "content": "Verify your email.",
    },
    ContentType.EMAIL_VERIFICATION_BODY: {
        "content": "Your verification code is {email_verification_code}.",
    },
    ContentType.EMAIL_RESET_PASSWORD_SUBJECT: {
        "content": "Reset Password.",
    },
    ContentType.EMAIL_RESET_PASSWORD_BODY: {
        "content": "Please click <a href=\"{password_verification_link}\">the link</a> to reset your password.",
    },
    # Sms
    ContentType.PHONE_VERIFICATION: {
        "content": "Your verification code is {phone_verification_code}",
    },
    ContentType.PHONE_VERIFICATION_2FA: {
        "content": "Your verification code is {phone_verification_code_2fa}",
    },
}
# fmt: on
