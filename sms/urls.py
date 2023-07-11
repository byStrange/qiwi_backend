from django.urls import path

from sms.views import SendOTPView, VerifyOTPView, ResendOTPView

app_name ="sms"

urlpatterns = [
    path("send_otp/<str:phone_number>/", SendOTPView.as_view(), name="send_otp"),
    path("resend_otp/", ResendOTPView.as_view(), name="resend_otp"),
    path("verify/", VerifyOTPView.as_view(), name="verify_otp")
]