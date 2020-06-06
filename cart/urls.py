from .views import *
from django.urls import path

app_name = 'cart'

urlpatterns = [
    path('homepage/', HomePageView.as_view(), name='homepage'),
    path('homepage/<str:prod_cat>/', Sub1View.as_view(), name='productcategory'),
    path('homepage/<str:prod_cat>/<str:product>/', FinalProductView.as_view(), name='individualproduct'),
]
