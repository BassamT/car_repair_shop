# Generated by Django 3.2.25 on 2024-12-04 10:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('repair_shop', '0008_invoice_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='public_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
