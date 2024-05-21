# Generated by Django 5.0.3 on 2024-05-20 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petStoreApp', '0034_delete_dashboarddata_delete_groomingreservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroomingReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=100)),
                ('pet_type', models.CharField(choices=[('Dog', 'Dog'), ('Cat', 'Cat')], max_length=50)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField(default='00:00:00')),
            ],
        ),
    ]