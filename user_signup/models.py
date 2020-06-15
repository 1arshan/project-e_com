from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random
from django.http import HttpResponse
from twilio.rest import Client
from medhistory.secrets import SmsToken


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
    instance.phone_number = "+91" + instance.phone_number
    instance.otp = random.randrange(10101, 909090)
    broadcast_sms(instance.otp, instance.phone_number)


def broadcast_sms(otp, phone_number):
    message_to_broadcast = ("verification code is: " + str(otp) + "\nthis code will valid for only 45 secs")
    client = Client(SmsToken.sid_key, SmsToken.secret_key)
    client.messages.create(to=phone_number,
                           from_=SmsToken.phone_number,
                           body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)
