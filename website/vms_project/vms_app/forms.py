from django import forms

vehicleTypes = (
    ('electric', 'Electric'),
    ('truck', 'Truck'),
    ('car', 'Car'),
    ('van', 'Van'),
)

vehicleStatusChoices = (
    ('active', 'Active'),
    ('non-active', 'Non-active'),
)

class loginForm(forms.Form):
    username = forms.CharField(label="", max_length=65, widget=forms.TextInput(attrs={"class":"form-control",
                                                                            "placeholder":"Username"}))
    password = forms.CharField(label="", max_length=65, widget=forms.PasswordInput(attrs={"class":"form-control",
                                                                                "placeholder":"Password"}))


class addDriverForm(forms.Form):
    username = forms.CharField(label='Username', max_length=65, widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='Password', max_length=65, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label='Email', max_length=65, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First name', max_length=65, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last name', max_length=65, widget=forms.TextInput(attrs={"class":"form-control"}))

    government_id = forms.CharField(label='IIN', widget=forms.TextInput(attrs={"class":"form-control"}))
    driving_license_code = forms.CharField(label='Driving License Code', widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={"class":"form-control"}))

class addTaskForm(forms.Form):
    driver_username = forms.CharField(label='Driver username', max_length=65, widget=forms.TextInput(attrs={"class":"form-control"}))
    point_a = forms.CharField(label='Point A', widget=forms.HiddenInput())
    point_b = forms.CharField(label='Point B', widget=forms.HiddenInput())

class addVehicleForm(forms.Form):
    make = forms.CharField(label='Make', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    year = forms.IntegerField(label='Year', widget=forms.NumberInput(attrs={"class":"form-control"}))
    license_plate = forms.CharField(label='License plate', max_length=30,
                                    widget=forms.TextInput(attrs={"class":"form-control"}))
    model = forms.CharField(label='Model', max_length=30,
                            widget=forms.TextInput(attrs={"class":"form-control"}))
    type = forms.ChoiceField(label='Type', choices=vehicleTypes,
                             widget=forms.Select(attrs={"class":"form-control"}))
    mileage = forms.IntegerField(label='Mileage', widget=forms.NumberInput(attrs={"class":"form-control"}))

class addMaintenanceOrFuelingPersonForm(forms.Form):
    lChoices = (
        ("Maintenance Person", "Maintenance Person"),
        ("Fueling Person", "Fueling Person"),
    )
    user_type = forms.ChoiceField(choices=lChoices, widget=forms.Select(attrs={"class":"form-control"}))
    username = forms.CharField(label='Username', max_length=65, widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='Password', max_length=65, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label='Email', max_length=65, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First name', max_length=65, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last name', max_length=65, widget=forms.TextInput(attrs={"class":"form-control"}))

class addFuelingInfoForm(forms.Form):
    license_plate = forms.CharField(label='License plate of car', max_length=30,
                                    widget=forms.TextInput(attrs={"class":"form-control"}))
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={"class":"form-control"}))
    gas_station_name = forms.CharField(label='Gas station', max_length=65,
                                       widget=forms.TextInput(attrs={"class":"form-control"}))
    fuel_amount = forms.FloatField(label='Amount of fuel', widget=forms.NumberInput(attrs={"class":"form-control"}))
    total_fuel_cost = forms.FloatField(label='Total fuel cost', widget=forms.NumberInput(attrs={"class":"form-control"}))
    # TODO think about this.
    image_before_fueling = forms.ImageField(label='Image before fueling',
                                            widget=forms.FileInput(attrs={"class":"form-control-file"}))
    image_after_fueling = forms.ImageField(label='Image after fueling',
                                           widget=forms.FileInput(attrs={"class":"form-control-file"}))

class reportRepairForm(forms.Form):
    replaced_part_number = forms.IntegerField(label='Replace part No',
                                              widget=forms.NumberInput(attrs={"class":"form-control"}))
    replaced_part_image = forms.ImageField(label="Image of replace part",
                                           widget=forms.FileInput(attrs={"class":"form-control-file"}))
    total_cost = forms.FloatField(label='Total cost',
                                  widget=forms.NumberInput(attrs={"class":"form-control"}))

class editMaintenanceForm(forms.Form):
    mileage = forms.IntegerField(label='Mileage', widget=forms.NumberInput(attrs={"class":"form-control"}))
    status = forms.ChoiceField(label='Status', choices=vehicleStatusChoices,
                               widget=forms.Select(attrs={"class":"form-control"}))

