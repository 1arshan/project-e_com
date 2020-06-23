from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random
from braodcaster.sms import PrepareSms
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, blank=True)
    date = models.DateTimeField(auto_now=True)


class TempUser(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)
    date = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=256)
    otp = models.CharField(max_length=8, blank=True)


@receiver(pre_save, sender=TempUser)
def create_sub1(sender, instance, **kwargs):
    instance.otp = random.randrange(10101, 909090)
    content = "verification code is: " + str(instance.otp) + "\nthis code will valid for only 45 secs"
    PrepareSms(instance.phone_number, content)

