from .serializers import TempUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import TempUser
from datetime import datetime, timezone
from .mail import sendmail
from .token import get_tokens_for_user
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from .token import account_activation_token
from django.contrib.auth.models import User


class TempUserView(APIView):

    def post(self, request):
        data = request.data
        try:
            t = TempUser.objects.get(phone_number="+91" + data['phone_number'])
            serializer = TempUserSerializer(t, data=data)

        except Exception:
            serializer = TempUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response("otp sent", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, ph_no):
        data = TempUser.objects.get(phone_number=ph_no)
        diff = datetime.now(timezone.utc) - data.date
        if diff.seconds > 20:
            data.otp = "1234"  # just a type of signal
            data.save()
            return Response("resend", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("wait", status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    def post(self, request, ph_no):
        otp_provided = request.data
        data = TempUser.objects.get(phone_number=ph_no)
        diff = datetime.now(timezone.utc) - data.date
        if diff.seconds < 50:
            if otp_provided["otp"] == data.otp:
                user = User.objects.create_user(username=data.phone_number, email=data.email,
                                                password=data.password, first_name=data.first_name,
                                                last_name=data.last_name)
                user.save()
                if user.email:
                    current_site = get_current_site(request)
                    sendmail(user, current_site)
                    mailotp = "please verify your mail also"
                else:
                    mailotp = "it will be better if you also provide us your email address"

                x = get_tokens_for_user(user)

                pr = "phone number verified  " \
                     + "\naccess token: " + x['access'] \
                     + "\nrefresh token: " + x['refresh'] \
                     + mailotp
                data.delete()

                return Response(pr, status=status.HTTP_202_ACCEPTED)
            return Response("OTP incorrect", status=status.HTTP_200_OK)
        return Response("OTP expire", status=status.HTTP_200_OK)


#do a redirection to login page
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Email_verified')
    else:
        return HttpResponse('Activation link is invalid!')
