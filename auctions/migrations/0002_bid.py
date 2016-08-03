# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-01 23:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('bid_name', models.IntegerField(primary_key=True, serialize=False)),
                ('bid_amt', models.IntegerField()),
                ('bid_time', models.DateTimeField()),
                ('auction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Items')),
            ],
        ),
    ]
