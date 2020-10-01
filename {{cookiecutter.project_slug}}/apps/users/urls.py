from django.urls import path

from apps.users.views import profile, reset_password, signin, signup

app_name = "apps.users"


urlpatterns = [
    # signin
    path("signin/", signin.SignInView.as_view(), name="signin"),
    path("signin/verify/2fa/", signin.SignIn2FAView.as_view(), name="signin-verify-2fa"),
    path("signout/", signin.SignOutView.as_view(), name="signout"),
    # reset password
    path("password/", reset_password.ResetPasswordView.as_view(), name="reset-password"),
    path(
        "password/verify/<slug:reset_password_code>/",
        reset_password.ResetPasswordVerifyView.as_view(),
        name="reset-password-verify",
    ),
    # signup
    path("signup/send/email/", signup.SignUpSendEmailView.as_view(), name="signup-send-email"),
    path("signup/verify/email/<uuid:pk>/", signup.SignUpVerifyEmailView.as_view(), name="signup-verify-email"),
    path("signup/send/sms/<uuid:pk>/", signup.SignUpSendSmsView.as_view(), name="signup-send-sms"),
    path("signup/verify/phone/<uuid:pk>/", signup.SignUpVerifyPhoneView.as_view(), name="signup-verify-phone"),
    path("signup/password/<uuid:pk>/", signup.SignUpPasswordView.as_view(), name="signup-password"),
    path("signup/profile/<uuid:pk>/", signup.SignUpProfileView.as_view(), name="signup-profile"),
    path("signup/finish/<uuid:pk>/", signup.SignUpFinishView.as_view(), name="signup-finish"),
    # profile
    path("profile/", profile.ProfileRetrieveView.as_view(), name="profile"),
    path("profile/update/", profile.ProfileUpdateView.as_view(), name="profile-update"),
    path("profile/password/", profile.ProfilePasswordView.as_view(), name="profile-password"),
    path("profile/destroy/", profile.ProfileDestroyView.as_view(), name="profile-destroy"),
    path("profile/send/email/", profile.ProfileSendVerificationEmailView.as_view(), name="profile-send-email"),
    path("profile/verify/email/", profile.VerifyEmailView.as_view(), name="profile-verify-email"),
    path("profile/send/sms/", profile.ProfileSendVerificationSmsView.as_view(), name="profile-send-sms"),
    path("profile/verify/phone/", profile.VerifyPhoneView.as_view(), name="profile-verify-phone"),
]
