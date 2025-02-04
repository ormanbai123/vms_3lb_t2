# Generated by Django 4.2.7 on 2023-11-29 19:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0012_alter_fuelinginfo_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('replaced_part_number', models.IntegerField()),
                ('replaced_part_image', models.ImageField(upload_to='maintenance/')),
                ('total_cost', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('maintenance_person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms_app.maintenanceperson')),
                ('vehicle_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms_app.vehicle')),
            ],
        ),
    ]
