from django.conf.urls import url
from django.urls import path
from . import views
from . import views2
urlpatterns = [
    path('signup/', views.TempUserView.as_view(), name='signup'),
    path('<str:ph_no>/resend/', views.TempUserView.as_view(), name='resend'),
    path('phone_number/verify/', views.VerifyOtpView.as_view(), name='verify'),
    path('password_reset/<str:medium>/', views2.PasswordResetView.as_view()),
    path('otp/login/', views2.otp_login_view,name='otplogin'),
    path('password_reset/otp/verify/', views2.PasswordResetOtpVerifyView.as_view(), name='otpverify'),
    url(r'^verify_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
    url(r'^new_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views2.reset_password, name='newpassword'),
]
