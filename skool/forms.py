from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    # dob= forms.DateField(widget=forms.DateInput(
    #     attrs={
    #         'placeholder': 'mm'+'-'+'yy'+'-'+'dd',
    # }
    # ))
    class Meta:
        model=User
        fields=['username','email','password1','password2',]


class NewsFeedForm(forms.ModelForm):
    class Meta:
        model=NewsFeed
        fields='__all__'
        exclude=['slug','date_added']



class TeacherProfileForm(forms.ModelForm):
    dob=forms.DateField(widget=forms.DateInput(
        attrs={
            'placeholder': 'mm'+'-'+'yy'+'-'+'dd',
    }
    )
    )
    class Meta:
        model=TeacherProfile
        fields='__all__'
        exclude=['date_added']

class StudentProfileForm(forms.ModelForm):
    # dob=forms.DateField(widget=forms.DateInput(
    #     attrs={
    #         'placeholder': 'mm'+'-'+'yy'+'-'+'dd',
    # }
    # )
    # )
    class Meta:
        model=StudentProfile
        fields= ['id_no','picture']
      

class ResultForm(forms.ModelForm):
    class Meta:
        model=Result
        fields='__all__'
        exclude=['date_added']
    