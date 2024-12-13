from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class create_account_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['fname','lname','username', 'email', 'password1', 'password2']
        widgets = {
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }


class user_role_form(ModelForm):
    class Meta:
        model = user_roles
        fields = ['role']
        widgets = {
            'role':forms.TextInput(attrs={'class': 'form-control'}),
            
}
        
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['fname','middle','lname','username','userrole','email', 'password1', 'password2']
        widgets = {
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'middle':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'userrole':forms.Select(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }


class profileform(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','fname','middle','lname','username','email','Contact']
        widgets = {
            'avatar':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'middle':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'Contact':forms.NumberInput(attrs={'class':'form-control'}),
        }


class calibrationsform(ModelForm):
    class Meta:
        model = calibrations
        fields = ['sensor_hieght','setting_height','low_threshold','mediun_threshold','heigh_threshold']
        widgets = {
            'sensor_hieght':forms.NumberInput(attrs={'class':'form-control'}),
            'setting_height':forms.NumberInput(attrs={'class':'form-control'}),
            'low_threshold':forms.NumberInput(attrs={'class':'form-control'}),
            'mediun_threshold':forms.NumberInput(attrs={'class':'form-control'}),
            'heigh_threshold':forms.NumberInput(attrs={'class':'form-control'}),
            
        }


