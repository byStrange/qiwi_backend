from django.db import models

# Create your models here.
class PhoneNumberVerification(models.Model):
    phone_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number
    