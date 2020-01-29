from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
#Don't worry about this file! 
class CustomUserCreationForm(UserCreationForm):
    #is_teacher = forms.BooleanField(label = "is_teacher")
    class Meta:
        model = CustomUser
        exclude = ()

class CustomUserChangeForm(UserChangeForm):
    #is_teacher = forms.BooleanField(label="is_teacher")
    class Meta:
        model = CustomUser
        exclude = ()