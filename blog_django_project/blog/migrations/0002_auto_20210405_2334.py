# Generated by Django 3.1.7 on 2021-04-05 23:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 5, 23, 34, 3, 962639, tzinfo=utc)),
        ),
    ]