# Generated by Django 4.2.7 on 2023-11-07 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('1', 'Admin_stuff'), ('2', 'Driver'), ('3', 'Maintenance_person'), ('4', 'Fueling_person')], default=1, max_length=30),
        ),
    ]
