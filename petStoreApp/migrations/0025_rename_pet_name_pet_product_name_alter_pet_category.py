# Generated by Django 5.0.3 on 2024-05-06 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0024_rename_name_id_pet_pet_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='pet_name',
            new_name='product_name',
        ),
        migrations.AlterField(
            model_name='pet',
            name='category',
            field=models.CharField(choices=[('Cat', 'Cat'), ('Dog', 'Dog'), ('Collars', 'Collars'), ('Toys', 'Toys'), ('Foods', 'Foods'), ('Grooming', 'Foods'), ('Clothing', 'Clothing'), ('Housing', 'Housing'), ('Health', 'Health')], max_length=100),
        ),
    ]
