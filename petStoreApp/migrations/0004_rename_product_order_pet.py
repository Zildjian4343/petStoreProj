
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0003_cartitem_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='pet',
        ),
    ]
