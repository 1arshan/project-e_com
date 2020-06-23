from .serializers import TempUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import TempUser, Profile
from datetime import datetime, timezone
from braodcaster.mail import MailVerification
from .token import get_tokens_for_user
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from .token import account_activation_token
from django.contrib.auth.models import User
from braodcaster.sms import PrepareSms
from braodcaster.mail import PrepareEmail
from django.core.exceptions import ObjectDoesNotExist
import random
from django.db.models import Q


# password reset ---------->
class PasswordResetView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.otp = random.randrange(10101, 909090)

    def post(self, request, medium):
        data = request.data
        t = User.objects.get(Q(username=data['username']) | Q(email=data['username']))
        if medium == 'sms':
            content = "verification code is: " + str(self.otp) + "\nthis code will valid for only 45 secs"
            try:
                PrepareSms(data['username'], content)
                Profile.objects.update_or_create(user=t, defaults={'user': t, 'otp': self.otp})
            except ObjectDoesNotExist:
                pass
            return Response("otp send to your number ,if not receive please check mobile number entered",
                            status=status.HTTP_200_OK)

        elif medium == 'email':
            try:
                content = str(
                    "<p>verification code is: " + str(self.otp) + "\nthis code will valid for only 45 secs</p>")
                PrepareEmail("Resset Your Account", content, data['username'])
                Profile.objects.update_or_create(user=t, defaults={'user': t, 'otp': self.otp})
            except ObjectDoesNotExist:
                pass
            return Response("otp send to your email ,if not receive please check email entered",
                            status=status.HTTP_200_OK)


# reset password otp send verification
class PasswordResetOtpVerifyView(APIView):
    def post(self, request):
        data = request.data
        try:
            t = User.objects.get(Q(username=data['username']) | Q(email=data['username']))
            diff = datetime.now(timezone.utc) - t.profile.date
            if data['otp'] == t.profile.otp and diff.seconds < 50:

                return Response("otp verified", status=status.HTTP_202_ACCEPTED)
            else:

                return Response("either otp provided is wrong or it expires", status=status.HTTP_200_OK)
        except ObjectDoesNotExist or Exception:
            return Response("either otp provided is wrong or it expires", status=status.HTTP_200_OK)


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
                    MailVerification(user, current_site)
                    mail_otp = "please verify your mail also"
                else:
                    mail_otp = "it will be better if you also provide us your email address"

                x = get_tokens_for_user(user)

                pr = str("phone number verified  " \
                         + "\naccess token: " + x['access'] \
                         + "\nrefresh token: " + x['refresh'] \
                         + mail_otp)
                data.delete()

                return Response(pr, status=status.HTTP_202_ACCEPTED)
            return Response("OTP incorrect", status=status.HTTP_200_OK)
        return Response("OTP expire", status=status.HTTP_200_OK)


# do a redirection to login page
# email verififcation
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('Activation link is invalid!', status=status.HTTP_400_BAD_REQUEST)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Profile.objects.create(user=user, email_verified=True)
        #login(request, user)
        return HttpResponse('Email_verified',status=status.HTTP_201_CREATED)
    else:
        return HttpResponse('Activation link is invalid!',status=status.HTTP_400_BAD_REQUEST)