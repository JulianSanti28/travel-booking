# Generated by Django 3.2.4 on 2021-10-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_booking', '0006_city_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
