# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-06 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_change_crated_at_default_to_timezone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='title',
            field=models.CharField(max_length=140, unique=True),
        ),
    ]
