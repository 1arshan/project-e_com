from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jwtauth.urls')),
    path('cart/', include('cart.urls')),
    path('signup/', include('user_signup.urls')),
    path('login/', include('user_signup.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root =settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)