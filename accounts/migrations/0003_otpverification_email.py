# Generated by Django 5.0.7 on 2024-08-01 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_otpverification_remove_customuser_is_verified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpverification',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
