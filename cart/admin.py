from django.contrib import admin
from .models import *
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin


@admin.register(Sub1)
class Sub1Admin(admin.ModelAdmin):
    list_display = ("name", "link",)
    list_filter = ("link",)


admin.site.register(CartObject)


@admin.register(FinalProduct)
class MyModelAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ("name", "link", "model_no",)
    list_filter = ("link",)
