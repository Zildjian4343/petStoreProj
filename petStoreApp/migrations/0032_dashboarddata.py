# Generated by Django 5.0.3 on 2024-05-19 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0031_alter_pet_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sales', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
    ]
