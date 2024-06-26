# Generated by Django 5.0.3 on 2024-05-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0008_accessory_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessory',
            name='image',
            field=models.ImageField(upload_to='pics'),
        ),
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.CharField(choices=[('Dry Food', 'Dry Food'), ('Wet Food', 'Wet Food'), ('Treats', 'Treats'), ('Poop Litter', 'Poop Litter')], default='Dry Food', max_length=100),
        ),
        migrations.AlterField(
            model_name='food',
            name='image',
            field=models.ImageField(upload_to='pics'),
        ),
    ]
