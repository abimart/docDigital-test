from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .models import Client
from django.core.exceptions import ValidationError
import re

def createClient(request):
    name = request.POST['nameInput']
    rfc = request.POST['rfcInput']
    telefono = request.POST['telefonoInput']

    client = Client.objects.create(
        name=name, rfc=rfc, telefono=telefono)
    messages.success(request, 'Cliente: ' + name +' ¡Guardado correctamente!')
    return redirect('/')

def editClient(request, slug):
    client = Client.objects.get(slug=slug)
    
    name = request.POST.get('nameInput')
    rfc = request.POST.get('rfcInput', None)
    telefono = request.POST.get('telefonoInput')
    if request.method == 'POST':

        client.name = name
        client.rfc = rfc
        client.telefono = telefono
        client.save()
        messages.success(request, 'Cliente: ' + name +' ¡Editado correctamente!')
        return redirect('/')

    return render (request, "users/edit.html", {"client": client})

def deleteClient(request, slug):
    client = Client.objects.get(slug=slug)

    client.delete()
    messages.success(request, 'Cliente borrado!')
    return redirect('/')  


def home(request):
    clients = Client.objects.all()
    return render(request, "users/home.html", {"clients": clients})

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            company = form.cleaned_data.get('company')
            messages.success(request, f'Cuenta creada por {company}')
            return redirect(to='login')
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        self.request.session.set_expiry(0)
        self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tu perfil se actualizó con éxito')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

