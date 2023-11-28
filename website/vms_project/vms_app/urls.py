
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='vms-index'),
    path("login/", views.userLogin, name='vms-login'),
    path("logout/", views.userLogout, name='vms-logout'),

    path("account/<username>", views.accountView, name='vms-account-view'),

    path("admin_home/", views.adminHome, name='vms-admin-home'),
    path("driver_home/", views.driverHome, name='vms-driver-home'),
    path("fueling_person_home/", views.fuelingPersonHome, name='vms-fueling-person-home'),
    path("maintenance_person_home/", views.maintenancePersonHome, name='vms-maintenance-person-home'),

    path("add_driver/", views.addDriver, name='vms-add-driver'),
    path("add_maintenanceorfuelingperson/", views.addMaintenanceOrFuelingPerson,
         name='vms-add-maintenanceorfuelingperson'),
    path("add_task/", views.addTask, name='vms-add-task'),
    path("add_vehicle/", views.addVehicle, name='vms-add-vehicle'),

    path("add_fueling_info/", views.addFuelingInfo, name='vms-add-fueling-info'),

    path("generic_Home/", views.genericHome, name='vms-generic-home'),
]

