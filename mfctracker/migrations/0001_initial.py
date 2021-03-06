# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 23:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('path', models.CharField(max_length=128, unique=True)),
                ('mergeinfo', jsonfield.fields.JSONField(default={})),
                ('last_revision', models.IntegerField(default=1)),
                ('branch_revision', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('revision', models.IntegerField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('mfc_after', models.DateField(blank=True, null=True)),
                ('msg', models.TextField()),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mfctracker.Branch')),
                ('merged_to', models.ManyToManyField(blank=True, related_name='merges', to='mfctracker.Branch')),
            ],
        ),
    ]
