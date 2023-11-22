from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.exceptions import PermissionDenied

from .models import CustomUser, Driver, Task, DriverTask, Vehicle, FuelingInfo
from .forms import loginForm, addDriverForm, addMaintenanceOrFuelingPersonForm, addTaskForm, addVehicleForm, \
    addFuelingInfoForm


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
            driver = CustomUser.objects.get(username=driver_username, user_type=CustomUser.DRIVER)
            if driver:
                task = Task.objects.create(pointA=point_a, pointB=point_b)
                DriverTask.objects.create(driver_id=driver.id, task_id=task.id)
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
                else:
                    user.user_type = CustomUser.FUELING_PERSON
                user.save()
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
                    fueling_person_id = request.user,
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
    return render(request, 'fueling_templates/add_fueling.html', {'form': form})
