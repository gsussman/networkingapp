# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-13 22:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('networking', '0004_connection_connection_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='networking.Connection')),
            ],
        ),
        migrations.RenameModel(
            old_name='Contact',
            new_name='Contacted',
        ),
    ]
