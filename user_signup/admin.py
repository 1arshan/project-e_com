from django.contrib import admin
from .models import *


# admin.site.register(TempUser)
@admin.register(TempUser)
class TempUserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "email",)
    readonly_fields = ('date',)

"""
@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ("link", "phone_number_verified", 'email_verified',)
"""