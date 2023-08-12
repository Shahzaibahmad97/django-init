# Generated by Django 4.2.4 on 2023-08-12 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_stylist_userprofile_stylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='salonprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='salon_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stylist',
            name='salon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stylists', to='users.salonprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
