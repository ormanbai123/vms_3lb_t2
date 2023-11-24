from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.driverLogin, name='api-login'),
    path("logout/", views.driverLogout, name='api-logout'),

    path("finish_task/", views.finishTask, name='api-finish-task'),
]


