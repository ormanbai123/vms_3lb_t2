from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from .models import Driver, Vehicle, MyAdmin, CustomUser, MaintenancePerson, FuelingPerson
from .models import Task, Route, DriverTask, DriverVehicle

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
admin.site.register(Driver)
admin.site.register(MyAdmin)
admin.site.register(MaintenancePerson)
admin.site.register(FuelingPerson)
admin.site.register(Vehicle)

admin.site.register(Task)
admin.site.register(Route)
admin.site.register(DriverTask)
admin.site.register(DriverVehicle)
