from django.http import HttpResponse
from twilio.rest import Client
from medhistory.secrets import SmsToken
import asyncio
from rest_framework.response import Response

async def broadcast_sms(phone_number, content):
    message_to_broadcast = content
    client = Client(SmsToken.sid_key, SmsToken.secret_key)
    phone_number = "+91" + phone_number
    client.messages.create(to=phone_number,
                           from_=SmsToken.phone_number,
                           body=message_to_broadcast)
    return Response("messages sent!", status=None)


def PrepareSms(phone_number, content):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(broadcast_sms(phone_number, content))
    loop.close()
    return 1
