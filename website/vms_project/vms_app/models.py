from django.db import models
from django.contrib.auth.models import AbstractUser
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
    objects = models.Manager()

class Task(models.Model):
    STATUS_CHOICES = [
        ("posted", "Posted"),
        ("completed", "Completed"),
        ("in_progress", "In progress"),
        ("declined", "Declined"),
    ]
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    pointA = models.TextField() # from
    pointB = models.TextField() # to
    status = models.TextField(choices=STATUS_CHOICES, default="posted")
    objects = models.Manager()

class DriverVehicle(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    objects = models.Manager()

class DriverTask(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    objects = models.Manager()