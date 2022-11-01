from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Comment
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(max_length=200)
    last_name=forms.CharField(max_length=200)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
class UserUpdate(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['photo']
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['body']               