from rest_framework import generics
from .models import FinalProduct, CartObject, Sub1
from .serializers import FinalProductSerializer, CartObjectSerializer, Sub1Serializer


class HomePageView(generics.ListAPIView):
    queryset = CartObject.objects.all()
    serializer_class = CartObjectSerializer


class Sub1View(generics.ListAPIView):
    serializer_class = Sub1Serializer

    def get_queryset(self):
        sub_category = self.kwargs['prod_cat']
        return Sub1.objects.filter(link=sub_category)


class FinalProductView(generics.ListAPIView):
    serializer_class = FinalProductSerializer

    def get_queryset(self):
        sub_cat = self.kwargs['product']
        return FinalProduct.objects.filter(link=sub_cat)
