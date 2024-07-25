# Generated by Django 4.2.10 on 2024-04-24 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api', '0007_predictinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionToken',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('token', models.CharField(max_length=500, null=True)),
                ('hostname', models.CharField(blank=True, max_length=100, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=100, null=True)),
                ('mac_address', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]