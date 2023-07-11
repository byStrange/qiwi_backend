from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from sms.models import PhoneNumberVerification
from main.models import BasicUser

from sms.functions import generate_otp, send_otp

class SendOTPView(APIView):
    def post(self, request, phone_number):
        try:
            number_verification = PhoneNumberVerification.objects.get(phone_number=phone_number)
            return Response(
                {"error": "Ushbu telefon raqamiga allaqachon sms jo'natilgan"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PhoneNumberVerification.DoesNotExist:
            try:
                user = BasicUser.objects.get(user__username=phone_number)
                return Response(
                    {"error": "Bu telefon raqami bilan allaqachon ro'yxatdan o'tilgan."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except BasicUser.DoesNotExist:
                otp = generate_otp()
                number_verification = PhoneNumberVerification(phone_number=phone_number)
                number_verification.otp = otp
                # send_otp(phone_nimber, otp)
                number_verification.save()
                return Response(
                    {"success": "OTP muvaffaqiyatli jo'natildi.", "request_id": number_verification.id ,"timestamp": number_verification.timestamp},
                    status=status.HTTP_200_OK
                )



class ResendOTPView(APIView):
    def post(self, request):
        try:
            request_id = request.data.get("request_id")
            number_verification = PhoneNumberVerification.objects.get(id=request_id)
            elapsed_time = timezone.now() - number_verification.timestamp
            if elapsed_time.total_seconds() < 120:
                remaining_time = 120 - elapsed_time.total_seconds()
                return Response(
                    {"error":f"Iltimos, yangi OTP so'rov qilishdan oldin {remaining_time:.0f} soniya kutib turing."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # Continue with sending the OTP
                otp = generate_otp()
                number_verification.otp = otp
                number_verification.timestamp = timezone.now()
                number_verification.save()
                return Response(
                    {"success": "OTP muvaffaqiyatli yuborildi.", "request_id": number_verification.id, "timestamp": number_verification.timestamp},
                    status=status.HTTP_200_OK
                )
        except PhoneNumberVerification.DoesNotExist:
            return Response(
                {"error": "Telefon raqami topilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )



class VerifyOTPView(APIView):
    def post(self, request):
        request_id = request.data.get('request_id')
        otp = request.data.get('otp')
        
        try:
            verification = PhoneNumberVerification.objects.get(id=request_id)
            if verification.otp == str(otp):
                verification.verified = True
                verification.save()
                return Response(
                    {"success": "OTP kodi tasdiqlandi"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Xato kod."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except PhoneNumberVerification.DoesNotExist:
            return Response(
                {"error": "Xato so'rov jo'natildi."},
                status=status.HTTP_400_BAD_REQUEST
            )