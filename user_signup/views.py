from .serializers import TempUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import TempUser, Profile
from datetime import datetime, timezone
from .token import get_tokens_for_user
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from .token import account_activation_token
from django.contrib.auth.models import User
from .tasks import send_parallel_mail
from django.utils.http import urlsafe_base64_encode
from braodcaster.mail import MailVerification

#temperory user model till phone number verified
class TempUserView(APIView):

    def post(self, request):
        data = request.data
        try:
            t = TempUser.objects.get(data['phone_number'])
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


# otp verify and tranfers user data,email verification if provided
class VerifyOtpView(APIView):
    def post(self, request):
        data_receive = request.data
        data = TempUser.objects.get(phone_number=data_receive['phone_number'])
        diff = datetime.now(timezone.utc) - data.date
        if diff.seconds < 50:
            if data_receive["otp"] == data.otp:
                user = User.objects.create_user(username=data.phone_number, email=data.email,
                                                password=data.password, first_name=data.first_name,
                                                last_name=data.last_name)
                user.save()
                if user.email:
                    current_site = get_current_site(request)
                    MailVerification(user, current_site)

                    #MailVerification(subject, html_content, receiver_email)

                    mail_otp = "please verify your mail also"
                else:
                    mail_otp = "it will be better if you also provide us your email address"

                x = get_tokens_for_user(user)
                msg = "phone number verified " + mail_otp
                x["message"] = msg

                data.delete()

                return Response(x, status=status.HTTP_202_ACCEPTED)
            return Response("OTP incorrect", status=status.HTTP_200_OK)
        return Response("OTP expire", status=status.HTTP_200_OK)


# do a redirection to login page
# email verififcation
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('Activation link is invalid!', status=status.HTTP_200_OK)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Profile.objects.create(user=user, email_verified=True)
        #login(request, user)
        return HttpResponse('Email_verified',status=status.HTTP_201_CREATED)
    else:
        return HttpResponse('Activation link is invalid!',status=status.HTTP_200_OK)