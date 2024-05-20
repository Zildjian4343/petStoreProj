
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0004_rename_product_order_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_completed',
            field=models.BooleanField(default='False'),
        ),
    ]
