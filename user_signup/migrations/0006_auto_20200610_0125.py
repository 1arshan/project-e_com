# Generated by Django 3.0.6 on 2020-06-09 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_signup', '0005_auto_20200610_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempuser',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]