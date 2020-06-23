# Generated by Django 3.0.6 on 2020-06-21 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_signup', '0010_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='email_confirm',
            new_name='email_verified',
        ),
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
