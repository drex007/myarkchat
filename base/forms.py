from django.forms import ModelForm
from django import forms
from .models import Room,User



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label= 'password')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email',  ] 
    