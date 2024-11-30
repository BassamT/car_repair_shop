from django.db import migrations, models
import uuid

def generate_unique_access_tokens(apps, schema_editor):
    Customer = apps.get_model('repair_shop', 'Customer')
    for customer in Customer.objects.all():
        customer.access_token = uuid.uuid4()
        customer.save(update_fields=['access_token'])

class Migration(migrations.Migration):

    dependencies = [
        ('repair_shop', '0004_customer_access_token'),
    ]

    operations = [
        migrations.RunPython(generate_unique_access_tokens),
    ]