from rest_framework import serializers
from .models import FinalProduct, CartObject, Sub1


class FinalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalProduct
        fields = '__all__'


class CartObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartObject
        fields = '__all__'


class Sub1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sub1
        fields = '__all__'
