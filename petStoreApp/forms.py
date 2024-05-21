from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pet
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from .models import Profile
from django import forms
from .models import GroomingReservation 




class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AddPet(ModelForm):
    class Meta:
        model = Pet
        fields = ['product_name', 'category', 'desc', 'price', 'image']


class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'mobile_number']
        

class GroomingReservationForm(forms.ModelForm):
    class Meta:
        model = GroomingReservation
        fields = ['pet_name', 'pet_type', 'appointment_date', 'appointment_time']