# Generated by Django 3.2.5 on 2021-07-30 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20210730_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='income',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
