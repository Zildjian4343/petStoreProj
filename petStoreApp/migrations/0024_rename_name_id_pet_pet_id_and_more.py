# Generated by Django 5.0.3 on 2024-05-06 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0023_rename_pet_id_pet_name_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='Name_id',
            new_name='pet_id',
        ),
        migrations.RenameField(
            model_name='pet',
            old_name='Product_name',
            new_name='pet_name',
        ),
    ]