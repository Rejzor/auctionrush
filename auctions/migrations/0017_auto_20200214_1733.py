# Generated by Django 3.0.3 on 2020-02-14 16:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20200214_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='deadline_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
