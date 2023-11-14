from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser, Driver
from .forms import loginForm, addDriverForm, addMaintenanceOrFuelingPersonForm

# Create your views here.

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
                if user.user_type == CustomUser.DRIVER:
                    return redirect('/driver_home/')
                elif user.user_type == CustomUser.FUELING_PERSON:
                    return redirect('/fueling_person_home/')
                elif user.user_type == CustomUser.MAINTENANCE_PERSON:
                    return redirect('/maintenance_person_home/')
                elif user.user_type == CustomUser.MY_ADMIN:
                    return redirect('/admin_home/')
            else:
                print('Error occurred in logging!!')
                messages.error(request, 'Invalid username or password! Please try again.')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = loginForm()
    return render(request, 'registration/login.html', {'form' : form})

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

def addTask():
    pass
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
    return HttpResponse('Welcome to Maintenance Person Page!')
def fuelingPersonHome(request):
    return HttpResponse('Welcome to Fueling Person Page!')
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
            raise Http404('Unauthorized access')
    except:
        raise Http404('Account does not exist')


    context = {'user' : user}
    return render(request, 'account_page.html', context=context)
