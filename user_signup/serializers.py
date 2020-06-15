from .models import TempUser
from rest_framework import serializers


class TempUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempUser
        fields = ['first_name','last_name','email','phone_number','password']
