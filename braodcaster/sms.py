from django.http import HttpResponse
from twilio.rest import Client
from medhistory.secrets import SmsToken


async def broadcast_sms(phone_number,content):
    message_to_broadcast = content
    client = Client(SmsToken.sid_key, SmsToken.secret_key)
    client.messages.create(to=phone_number,
                           from_=SmsToken.phone_number,
                           body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)
