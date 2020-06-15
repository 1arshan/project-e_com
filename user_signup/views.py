from .serializers import TempUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import TempUser
from datetime import datetime, timezone
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TempUserView(APIView):

    def post(self, request):
        data = request.data
        try:
            t = TempUser.objects.get(phone_number="+91" +data['phone_number'])
            print(t)
            serializer = TempUserSerializer(t, data=data)

        except t.DoesNotExist:
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
                x = get_tokens_for_user(user)

                pr = "phone number verified  " \
                     + "\naccess token: " + x['access'] \
                     + "\nrefresh token: " + x['refresh']
                data.delete()

                return Response(pr, status=status.HTTP_202_ACCEPTED)
            return Response("OTP incorrect", status=status.HTTP_200_OK)
        return Response("OTP expire", status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
