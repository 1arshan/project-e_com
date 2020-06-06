from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


def renaming_uploaded_image1(instance, filename):
    return "cart_object/" + instance.name + ".png"


def renaming_uploaded_image2(instance, filename):
    return "sub_1/" + instance.name + ".png"


def renaming_uploaded_image3(instance, filename):
    return "final_product/" + instance.name + ".png"


class CartObject(models.Model):
    name = models.CharField(max_length=25, unique=True, primary_key=True)
    image = models.ImageField(blank=True, upload_to=renaming_uploaded_image1)

    def __str__(self):
        return f'{self.name}'


class Sub1(models.Model):
    name = models.CharField(max_length=35, unique=True, primary_key=True)
    photo = models.ImageField(blank=True, upload_to=renaming_uploaded_image2)
    link = models.ForeignKey(CartObject, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.name} '


class FinalProduct(models.Model):
    name = models.CharField(max_length=100)
    link = models.ForeignKey(Sub1, on_delete=models.CASCADE)
    specification = ArrayField(models.CharField(max_length=20, blank=True), blank=True)
    photo = models.ImageField(upload_to=renaming_uploaded_image3)
    diffrent_type = ArrayField(models.CharField(max_length=20, blank=True, default="NULL"), blank=True)
    prize = ArrayField(models.CharField(max_length=20, blank=True), blank=True)
    item_left = ArrayField(models.CharField(max_length=20, blank=True), blank=True)
    model_no = models.CharField(max_length=20, default="no model found")

    def __str__(self):
        return f'item name: {self.name}'


@receiver(pre_save, sender=Sub1)
def create_sub1(sender, instance, **kwargs):
    if instance.name.find(instance.link.name) == -1:
        instance.name = instance.name + "_" + instance.link.name


@receiver(pre_save, sender=FinalProduct)
def create_final_product(sender, instance, **kwargs):
    if instance.name.find(instance.link.name) == -1:
        instance.name = instance.name + "_" + instance.link.name
