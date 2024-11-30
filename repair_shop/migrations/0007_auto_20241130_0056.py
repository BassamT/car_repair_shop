# Generated by Django 3.2.25 on 2024-11-30 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repair_shop', '0006_alter_customer_access_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='access_token',
        ),
        migrations.AlterField(
            model_name='accesstoken',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_tokens', to='repair_shop.customer'),
        ),
    ]
