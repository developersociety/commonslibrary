# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0007_change_slug_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='privacy',
            field=models.ManyToManyField(blank=True, related_name='resources_privacy', to='directory.Organisation'),
        ),
    ]
