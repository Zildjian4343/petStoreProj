# Generated by Django 5.0.3 on 2024-05-06 12:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0014_petproduct_delete_petproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='petStoreApp.petproduct'),
        ),
    ]