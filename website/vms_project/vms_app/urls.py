
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.userLogin, name='login'),
    path("logout/", views.userLogout, name='logout'),

    #path("user/<id>", views.),

    path("admin_home/", views.adminHome, name='admin_home'),
    path("driver_home/", views.driverHome, name='driver_home'),
    path("fueling_person_home/", views.fuelingPersonHome, name='fueling_person_home'),


    path("add_driver/", views.addDriver, name='add_driver'),
    path("add_maintenanceorfuelingperson/", views.addMaintenanceOrFuelingPerson,
         name='add_maintenanceorfuelingperson'),
]

