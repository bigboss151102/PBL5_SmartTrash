# Generated by Django 4.2.10 on 2024-05-06 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_sessiontoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='garbagecompartment',
            old_name='name_compartment',
            new_name='type_name_compartment',
        ),
        migrations.RenameField(
            model_name='predictinfo',
            old_name='type_garbage',
            new_name='type_name_garbage',
        ),
        migrations.AddField(
            model_name='garbage',
            name='distance_is_full',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='garbagecompartment',
            name='distance_is_full',
            field=models.FloatField(default=0.0),
        ),
        migrations.DeleteModel(
            name='SessionToken',
        ),
    ]
