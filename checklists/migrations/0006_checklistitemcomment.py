# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-08-09 20:59
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checklists', '0005_auto_20170809_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChecklistItemComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklists.ChecklistItem')),
            ],
        ),
    ]
