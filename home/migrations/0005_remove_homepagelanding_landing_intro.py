# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-31 20:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_homepagerelatedlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagelanding',
            name='landing_intro',
        ),
    ]
