# Generated by Django 5.0.7 on 2024-08-01 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_language_alter_customuser_usertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpverification',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]
