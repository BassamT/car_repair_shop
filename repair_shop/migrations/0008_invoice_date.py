# Generated by Django 3.2.25 on 2024-12-04 09:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('repair_shop', '0007_auto_20241130_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
