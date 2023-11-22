from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    MY_ADMIN = '1'
    DRIVER = '2'
    MAINTENANCE_PERSON = '3'
    FUELING_PERSON = '4'

    user_type_data = ((MY_ADMIN, "Admin_stuff"),
                      (DRIVER, "Driver"),
                      (MAINTENANCE_PERSON, "Maintenance_person"),
                      (FUELING_PERSON, "Fueling_person"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=30)


class MyAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()

class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    government_id = models.TextField()
    driving_license_code = models.TextField()
    phone_number = models.TextField()
    objects = models.Manager()

class MaintenancePerson(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()

class FuelingPerson(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.TextField() # make = brand (e.g. Chevrolet, Lexus, Toyota)
    year = models.IntegerField()
    license_plate = models.TextField()
    model = models.TextField()
    type = models.TextField()
    mileage = models.IntegerField()
    status = models.TextField(default="active")
    objects = models.Manager()

class Task(models.Model):
    STATUS_CHOICES = [
        ("posted", "Posted"),
        ("completed", "Completed"),
        ("declined", "Declined"),
    ]
    id = models.AutoField(primary_key=True)
    pointA = models.TextField() # from
    pointB = models.TextField() # to
    status = models.TextField(choices=STATUS_CHOICES, default="posted")
    dateTaken = models.DateTimeField(default=timezone.now)
    objects = models.Manager()

class DriverVehicle(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    objects = models.Manager()

class DriverTask(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    objects = models.Manager()

class FuelingInfo(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    fueling_person_id = models.ForeignKey(FuelingPerson, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    gas_station_name = models.TextField()
    fuel_amount = models.FloatField()
    total_fuel_cost = models.FloatField()
    # TODO think about this.
    image_before_fueling = models.ImageField(upload_to="fueling")
    image_after_fueling = models.ImageField(upload_to="fueling")
    objects = models.Manager()


