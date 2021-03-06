# Generated by Django 3.0.6 on 2020-06-03 15:23

import cart.models
from django.db import migrations, models
import django.db.models.deletion
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartObject',
            fields=[
                ('name', models.CharField(max_length=25, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(blank=True, upload_to=cart.models.renaming_uploaded_image1)),
            ],
        ),
        migrations.CreateModel(
            name='Sub1',
            fields=[
                ('name', models.CharField(max_length=35, primary_key=True, serialize=False, unique=True)),
                ('photo', models.ImageField(blank=True, upload_to=cart.models.renaming_uploaded_image2)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.CartObject')),
            ],
        ),
        migrations.CreateModel(
            name='FinalProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('specification', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), blank=True, size=None)),
                ('photo', models.ImageField(upload_to=cart.models.renaming_uploaded_image3)),
                ('diffrent_type', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, default='NULL', max_length=20), blank=True, size=None)),
                ('prize', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), blank=True, size=None)),
                ('item_left', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), blank=True, size=None)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Sub1')),
            ],
        ),
    ]
