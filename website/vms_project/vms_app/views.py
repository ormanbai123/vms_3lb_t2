from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.exceptions import PermissionDenied
from django.views.generic import DeleteView

from .models import CustomUser, Driver, Task, DriverTask, Vehicle, FuelingInfo, RepairReport, FuelingPerson, \
    MaintenancePerson
from .forms import loginForm, addDriverForm, addMaintenanceOrFuelingPersonForm, addTaskForm, addVehicleForm, \
    addFuelingInfoForm, editMaintenanceForm, reportRepairForm


# Create your views here.

@login_required(login_url="/login/")
def genericHome(request):
    if request.user.user_type == CustomUser.MY_ADMIN:
        return redirect('/admin_home/')
    elif request.user.user_type == CustomUser.FUELING_PERSON:
        return redirect('/fueling_person_home')
    elif request.user.user_type == CustomUser.MAINTENANCE_PERSON:
        return redirect('/maintenance_person_home')
    else:
        return redirect('/driver_home')

def index(request):
    #TODO implement index page
    return redirect('login/')

def userLogin(request):
    form = None
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user = authenticate(request, username=username, password=password)
            user = CustomUser.objects.filter(username=username, password=password).last()
            if user:
                login(request, user)
                return genericHome(request)
            else:
                print('Error occurred in logging!!')
                messages.error(request, 'Invalid username or password! Please try again.')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = loginForm()
    return render(request, 'registration/login.html', {'form' : form})

@login_required(login_url="/login/")
def addVehicle(request):
    if request.user.user_type != CustomUser.MY_ADMIN:
        raise PermissionDenied()

    form = None
    if request.method == 'POST':
        form = addVehicleForm(request.POST)
        if form.is_valid():
            make = form.cleaned_data['make']
            year = form.cleaned_data['year']
            license_plate = form.cleaned_data['license_plate']
            model = form.cleaned_data['model']
            type = form.cleaned_data['type']
            mileage = form.cleaned_data['mileage']
            if year < 2005 or year > 2023:
                messages.error(request, "Invalid year!")
                return render(request, "admin_templates/add_vehicle_page.html", {"form":form})
            if mileage < 0:
                messages.error(request, "Invalid mileage!")
                return render(request, "admin_templates/add_vehicle_page.html", {"form":form})
            if Vehicle.objects.filter(license_plate=license_plate).exists():
                messages.error(request, "Car with this license plate already exists!")
                return render(request, "admin_templates/add_vehicle_page.html", {"form":form})

            Vehicle.objects.create(
                make=make,
                year=year,
                license_plate=license_plate,
                model=model,
                type=type,
                mileage=mileage
            )
            form = addVehicleForm()
            messages.success(request, "Car added successfully!")
        else:
            messages.error(request, "Invalid form!")
    else:
        form = addVehicleForm()
    return render(request, "admin_templates/add_vehicle_page.html", {"form":form})

@login_required(login_url="/login/")
def addDriver(request):
    form = None
    if request.method == 'POST':
        form = addDriverForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            government_id = form.cleaned_data['government_id']
            driving_license_code = form.cleaned_data['driving_license_code']
            phone_number = form.cleaned_data['phone_number']

            if CustomUser.objects.filter(username=username).exists():
                # User already exists
                messages.error(request, 'User with this username already exists')
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'User with this email already exists')
            else:
                user = CustomUser()
                user.username = username
                user.password = password
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.user_type = CustomUser.DRIVER
                user.save()
                Driver.objects.create(profile=user,
                                      government_id=government_id,
                                      driving_license_code=driving_license_code,
                                      phone_number=phone_number)
                messages.success(request,'Driver created successfully')
        else:
            print('Something went wrong')
            messages.error(request, 'Form invalid')
    else:
        form = addDriverForm()
    return render(request, 'admin_templates/add_driver_page.html', {'form':form})

@login_required(login_url="/login/")
def addTask(request):
    # TODO
    #  Finish this

    form = None
    if request.method == 'POST':
        form = addTaskForm(request.POST)
        if form.is_valid():
            driver_username = form.cleaned_data['driver_username']
            point_a = form.cleaned_data['point_a']
            point_b = form.cleaned_data['point_b']
            user = CustomUser.objects.get(username=driver_username, user_type=CustomUser.DRIVER)
            if user:
                driver = Driver.objects.get(profile=user)
                task = Task.objects.create(pointA=point_a, pointB=point_b)
                DriverTask.objects.create(driver_id=driver, task_id=task)
                messages.success(request, 'Task added successfully!')
            else:
                messages.error(request,'Driver with this username does not exist!')
    else:
        form = addTaskForm()
    return render(request, 'admin_templates/add_task_page.html', context={'form':form})

@login_required(login_url="/login/")
def addMaintenanceOrFuelingPerson(request):
    form = None
    if request.method == 'POST':
        form = addMaintenanceOrFuelingPersonForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_type = form.cleaned_data['user_type']

            if CustomUser.objects.filter(username=username).exists():
                # User already exists
                messages.error(request, 'User with this username already exists')
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'User with this email already exists')
            else:
                user = CustomUser()
                user.username = username
                user.password = password
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                if user_type == 'Maintenance Person':
                    user.user_type = CustomUser.MAINTENANCE_PERSON
                    user.save()
                    MaintenancePerson.objects.create(profile=user)
                else:
                    user.user_type = CustomUser.FUELING_PERSON
                    user.save()
                    FuelingPerson.objects.create(profile=user)
                form = addMaintenanceOrFuelingPersonForm()
                messages.success(request, 'User created successfully')
        else:
            print('Something went wrong')
            messages.error(request, 'Form invalid')
    else:
        form = addMaintenanceOrFuelingPersonForm()
    return render(request, 'admin_templates/add_maintenanceorfuelingperson_page.html', {'form': form})
@login_required(login_url="/login/")
def adminHome(request):
    return render(request, 'admin_templates/home.html',
                  {'user':request.user})

def driverHome(request):
    return HttpResponse('Welcome to Driver Page!')

def maintenancePersonHome(request):
    return render(request, "maintenance_templates/home.html",{'user':request.user})
def fuelingPersonHome(request):
    return render(request, "fueling_templates/home.html", {'user': request.user})
@login_required(login_url="/login/")
def userLogout(request):
    logout(request)
    return redirect('/login/')
@login_required(login_url="/login/")
def accountView(request, username):
    try:
        if request.user.username == username:
            user = CustomUser.objects.get(username=username)
        else:
            raise PermissionDenied()
    except:
        raise Http404('Account does not exist')


    context = {'user' : user}
    return render(request, 'account_page.html', context=context)

@login_required(login_url="/login/")
def addFuelingInfo(request):
    #TODO finish this
    if request.user.user_type != CustomUser.FUELING_PERSON:
        raise PermissionDenied
    form = None
    if request.method == 'POST':
        form = addFuelingInfoForm(request.POST, request.FILES)
        if form.is_valid():
            license_plate = form.cleaned_data['license_plate']
            date = form.cleaned_data['date']
            gas_station_name = form.cleaned_data['gas_station_name']
            fuel_amount = form.cleaned_data['fuel_amount']
            total_fuel_cost = form.cleaned_data['total_fuel_cost']
            image_before_fueling = form.cleaned_data['image_before_fueling']
            image_after_fueling = form.cleaned_data['image_after_fueling']

            vehicle = Vehicle.objects.filter(license_plate=license_plate).last()
            if vehicle is None:
                messages.error(request, 'Such car does not exist!')
            else:
                FuelingInfo.objects.create(
                    vehicle_id = vehicle,
                    fueling_person_id = FuelingPerson.objects.get(profile=request.user),
                    date = date,
                    gas_station_name = gas_station_name,
                    fuel_amount = fuel_amount,
                    total_fuel_cost = total_fuel_cost,
                    image_before_fueling = image_before_fueling,
                    image_after_fueling = image_after_fueling
                )
                form = addFuelingInfoForm()
                messages.success(request, "Fueling report added!")
        else:
            print('Something went wrong')
            messages.error(request, 'Form invalid')
    else:
        form = addFuelingInfoForm()
    return render(request, 'fueling_templates/add_fueling_page.html', {'form': form})

@login_required(login_url="/login/")
def reportRepair(request, vehicle_id):
    if request.user.user_type != CustomUser.MAINTENANCE_PERSON:
        raise PermissionDenied

    vehicle = Vehicle.objects.get(id=vehicle_id)

    form = None
    if request.method == 'POST':
        form = reportRepairForm(request.POST, request.FILES)
        if form.is_valid():
            replaced_part_number = form.cleaned_data['replaced_part_number']
            replaced_part_image = form.cleaned_data['replaced_part_image']
            total_cost = form.cleaned_data['total_cost']

            RepairReport.objects.create(
                vehicle_id = vehicle,
                maintenance_person_id = MaintenancePerson.objects.get(profile=request.user),
                total_cost=total_cost,
                replaced_part_image = replaced_part_image,
                replaced_part_number=replaced_part_number,
            )
            form = reportRepairForm()
            messages.success(request, "Fueling report added!")
        else:
            print('Something went wrong')
            messages.error(request, 'Form invalid')
    else:
        form = reportRepairForm()
    return render(request, 'maintenance_templates/repair_report.html',
                  {'form': form,'vehicle':vehicle})

@login_required(login_url="/login/")
def editMaintenanceInfo(request, vehicle_id):
    if request.user.user_type != CustomUser.MAINTENANCE_PERSON:
        raise PermissionDenied

    vehicle = Vehicle.objects.get(id=vehicle_id)
    if vehicle is None:
        messages.error(request, 'Such car does not exist!')

    form = None
    if request.method == 'POST':
        form = editMaintenanceForm(request.POST)
        if form.is_valid():
            mileage = form.cleaned_data['mileage']
            status = form.cleaned_data['status']

            Vehicle.objects.update(mileage=mileage,
                                   status=status)
            form = editMaintenanceForm()
            return redirect('/vehicle_list_view')
        else:
            print('Something went wrong')
            messages.error(request, 'Form invalid')
    else:
        form = editMaintenanceForm(initial={"mileage":vehicle.mileage,
                                            "status":vehicle.status})
    return render(request, 'maintenance_templates/edit_maintenance.html',
                  {'form': form, 'vehicle':vehicle})

@login_required(login_url="/login/")
def vehicleListView(request):
    vehicles = Vehicle.objects.all().order_by('id')
    if request.user.user_type == CustomUser.MY_ADMIN:
        return render(request, "admin_templates/vehicle_list.html",{'vehicles':vehicles})
    elif request.user.user_type == CustomUser.MAINTENANCE_PERSON:
        return render(request, "maintenance_templates/vehicle_list.html", {'vehicles':vehicles})
    else:
        return render(request, "fueling_templates/vehicle_list.html", {'vehicles':vehicles})
@login_required(login_url="/login/")
def userListView(request):
    if request.user.user_type != CustomUser.MY_ADMIN:
        raise PermissionDenied
    users = CustomUser.objects.exclude(user_type=CustomUser.MY_ADMIN).order_by('id')
    return render(request, "admin_templates/user_list.html", {'users':users})

@login_required(login_url="/login/")
def taskListView(request):
    if request.user.user_type != CustomUser.MY_ADMIN:
        raise PermissionDenied
    driver_task_dict = dict()
    for i in DriverTask.objects.all():
        driver_task_dict[i.task_id] = i.driver_id
    return render(request, "admin_templates/task_list.html",
                  {'driver_task_dict':driver_task_dict})

@login_required(login_url="/login/")
def fuelingInfoView(request):
    if request.user.user_type != CustomUser.FUELING_PERSON:
        raise PermissionDenied
    fueling_person = FuelingPerson.objects.get(profile=request.user)
    fueling_infos = FuelingInfo.objects.filter(fueling_person_id=fueling_person).all()
    return render(request, "fueling_templates/fueling_info.html",
                  {'infos':fueling_infos})

@login_required(login_url="/login/")
def repairReportView(request):
    if request.user.user_type != CustomUser.MAINTENANCE_PERSON:
        raise PermissionDenied
    maintenance_person = MaintenancePerson.objects.get(profile=request.user)
    reports = RepairReport.objects.filter(maintenance_person_id=maintenance_person).all()
    return render(request, "maintenance_templates/repair_reports.html",
                  {'reports':reports})

class VehicleDeleteView(DeleteView):
    model = Vehicle
    success_url = "/vehicle_list_view"
    template_name = "vehicle_delete.html"

class UserDeleteView(DeleteView):
    model = CustomUser
    success_url = "/user_list_view"
    template_name = "admin_templates/user_delete.html"

class TaskDeleteView(DeleteView):
    model = Task
    success_url = "/task_list_view"
    template_name = "admin_templates/task_delete.html"
