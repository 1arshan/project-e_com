# Generated by Django 3.0.6 on 2020-06-07 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_signup', '0002_tempuser_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempuser',
            name='password',
            field=models.CharField(default='null', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tempuser',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
