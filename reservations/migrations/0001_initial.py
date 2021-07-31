# Generated by Django 3.2.5 on 2021-07-28 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat', models.CharField(max_length=200)),
                ('city', models.CharField(choices=[('LONDON', 'LONDON'), ('PARIS', 'PARIS'), ('PORTO', 'PORTO')], max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('income', models.IntegerField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.location')),
            ],
        ),
    ]