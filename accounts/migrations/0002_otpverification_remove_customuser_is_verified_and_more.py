# Generated by Django 5.0.7 on 2024-08-01 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_expiration', models.DateTimeField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='otp',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='otp_expiration',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone',
        ),
    ]
