from django import forms


class loginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={"class":"form-control"}))


class addDriverForm(forms.Form):
    username = forms.CharField(label='Username', max_length=65)
    password = forms.CharField(label='Password', max_length=65, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=65)
    first_name = forms.CharField(label='First name', max_length=65)
    last_name = forms.CharField(label='Last name', max_length=65)

    government_id = forms.CharField(label='IIN')
    driving_license_code = forms.CharField(label='Driving License Code')
    phone_number = forms.CharField(label='Phone number')