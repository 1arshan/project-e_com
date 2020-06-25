from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Profile
from datetime import datetime, timezone
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from .token import account_activation_token
from django.contrib.auth.models import User
from braodcaster.sms import PrepareSms
from django.core.exceptions import ObjectDoesNotExist
import random
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode
from rest_framework.decorators import api_view
from .token import get_tokens_for_user
from braodcaster.tasks import send_parallel_mail

@api_view(['POST'])
def otp_login_view(request):
    data = request.data
    try:
        t = User.objects.get(Q(username=data['username']) | Q(email=data['username']))
        diff = datetime.now(timezone.utc) - t.profile.date
        if data['otp'] == t.profile.otp and diff.seconds < 5000:
            x = get_tokens_for_user(t)
            return Response(x, status=status.HTTP_202_ACCEPTED)
        else:
            return Response("either otp provided is wrong or it expires", status=status.HTTP_200_OK)
    except ObjectDoesNotExist or Exception:
        return Response("either otp provided is wrong or it expires", status=status.HTTP_200_OK)


# inserting new password
@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('Activation link is invalid!', status=status.HTTP_400_BAD_REQUEST)
    if user is not None and account_activation_token.check_token(user, token):
        data = request.data
        if data['new_password'] == data['confirm_password']:
            user.set_password(data['new_password'])
            user.save()
        else:
            return HttpResponse('new password and confirm password are not same', status=status.HTTP_201_CREATED)
        return HttpResponse('Password Reset', status=status.HTTP_201_CREATED)
    else:
        return HttpResponse('link is invalid!', status=status.HTTP_400_BAD_REQUEST)


# reset password otp send verification
class PasswordResetOtpVerifyView(APIView):
    def post(self, request):
        data = request.data
        try:
            t = User.objects.get(Q(username=data['username']) | Q(email=data['username']))
            diff = datetime.now(timezone.utc) - t.profile.date
            if data['otp'] == t.profile.otp and diff.seconds < 50:
                token = account_activation_token.make_token(t)
                domain = get_current_site(request).domain
                uid = urlsafe_base64_encode(force_bytes(t.pk))
                ot_link = 'http://' + domain + '/' + 'signup/new_password/' + uid + '/' + token + '/'
                print(ot_link)
                return Response(ot_link)

            else:

                return Response("either otp provided is wrong or it expires", status=status.HTTP_200_OK)
        except ObjectDoesNotExist or Exception:
            return Response("either otp provided is wrong or it expires", status=status.HTTP_200_OK)


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
                send_parallel_mail.delay("Resset Your Account", content, data['username'])
                Profile.objects.update_or_create(user=t, defaults={'user': t, 'otp': self.otp})
            except ObjectDoesNotExist:
                pass
            return Response("otp send to your email ,if not receive please check email entered",
                            status=status.HTTP_200_OK)
