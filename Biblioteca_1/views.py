from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect, render

from .models import Usuario


class LoginForm(AuthenticationForm):
    """Formulario de login personalizado con mejor presentación"""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
        })
    )

    class Meta:
        model = Usuario
        fields = ('username', 'password')


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


def login_view(request):
    """Vista de login personalizado con manejo de roles"""
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # El usuario es autenticado con su rol asociado
            return redirect('inicio')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'Biblioteca_1/login.html', context)


def inicio(request):
    """Vista de inicio que muestra el rol del usuario autenticado"""
    context = {}
    if request.user.is_authenticated:
        context['rol_usuario'] = request.user.rol
    return render(request, 'Biblioteca_1/home.html', context)


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
