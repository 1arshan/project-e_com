from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.TempUserView.as_view(), name='signup'),
    path('<str:ph_no>/resend/', views.TempUserView.as_view(), name='resend'),
    path('<str:ph_no>/verify/', views.VerifyOtpView.as_view(), name='verify'),
]

