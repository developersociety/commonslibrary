# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-06 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
        ('accounts', '0002_add_more_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organisations',
            field=models.ManyToManyField(blank=True, null=True, to='directory.Organisation'),
        ),
    ]
