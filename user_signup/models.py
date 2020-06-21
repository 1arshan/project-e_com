from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random
from braodcaster.sms import broadcast_sms
from django.contrib.auth.models import User
import asyncio

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirm = models.BooleanField(default=False)


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
    if instance.phone_number.find('+91', 0, 3) == -1:
        instance.phone_number = "+91" + instance.phone_number
    instance.otp = random.randrange(10101, 909090)
    content = "verification code is: " + str(instance.otp) + "\nthis code will valid for only 45 secs"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(broadcast_sms(instance.phone_number, content))
    loop.close()

