# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-29 23:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mfctracker', '0004_change'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='mfctracker.Commit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
