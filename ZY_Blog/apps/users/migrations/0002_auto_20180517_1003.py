# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-17 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EamilRecord',
            new_name='EmailRecord',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(default='tVDXne6q', max_length=50, verbose_name='昵称'),
        ),
    ]