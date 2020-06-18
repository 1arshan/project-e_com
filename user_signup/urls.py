from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.TempUserView.as_view(), name='signup'),
    path('<str:ph_no>/resend/', views.TempUserView.as_view(), name='resend'),
    path('<str:ph_no>/verify/', views.VerifyOtpView.as_view(), name='verify'),
    url(r'^verify_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
]

