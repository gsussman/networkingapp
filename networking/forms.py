from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Connection
from django.forms import ModelForm, modelform_factory


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1', 'password2', )
        
class ConnectionType(ModelForm):
    class Meta:
        model = Connection
        fields = ('connection_level', 'connection_type',)
        
class ConnectionLevel(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)