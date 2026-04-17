from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .models import Usuario


class RegistroForm(UserCreationForm):
    rol = forms.ChoiceField(
        choices=[
            (Usuario.ROL_CHOICES[1][0], Usuario.ROL_CHOICES[1][1]),  # USUARIO
            (Usuario.ROL_CHOICES[2][0], Usuario.ROL_CHOICES[2][1]),  # EMPLEADO
        ],
        label='Rol',
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'rol', 'password1', 'password2')


def inicio(request):
    return render(request, 'Biblioteca_1/home.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroForm()

    return render(request, 'Biblioteca_1/register.html', {'form': form})
