# Generated by Django 3.2.25 on 2024-11-29 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_shop', '0002_activitylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
