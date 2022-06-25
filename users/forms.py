from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    # Empresa ,Correo, RFC, Contraseña.
    company = forms.CharField(max_length=50,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Company',
                                                               'class': 'form-control',
                                                               }))
    rfc = forms.CharField(max_length=13,
                               min_length=12,
                               required=True,
                               validators=[
                                        RegexValidator(regex=r"^([a-zA-Z&Ñ]{3,4}\d{6}[a-zA-Z0-9]{3})$", message="RFC invalido")
                                    ],
                               widget=forms.TextInput(attrs={'placeholder': 'RFC',
                                                             'class': 'form-control',
                                                             }))
    username = forms.EmailField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    

    class Meta:
        
        model = User
        fields = ['company', 'rfc', 'username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))

    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateUserForm(forms.ModelForm):
    rfc = forms.CharField(max_length=13,
                               min_length=12,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['rfc', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['avatar']
