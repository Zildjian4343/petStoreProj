# Generated by Django 5.0.3 on 2024-05-06 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0022_delete_petproduct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='pet_id',
            new_name='Name_id',
        ),
        migrations.RenameField(
            model_name='pet',
            old_name='pet_name',
            new_name='Product_name',
        ),
    ]
