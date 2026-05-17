from datetime import timedelta

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import Usuario, Libro, Prestamo


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


def logout_view(request):
    logout(request)
    return redirect('inicio')


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


def lista_libros(request):
    """Listado de todos los libros"""
    libros = Libro.objects.all()
    context = {'libros': libros}
    return render(request, 'Biblioteca_1/libros.html', context)


def detalle_libro(request, id):
    """Detalle de un libro específico"""
    libro = get_object_or_404(Libro, id=id)
    context = {'libro': libro}
    return render(request, 'Biblioteca_1/detalle_libro.html', context)


def reservar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method != 'POST' or not request.user.is_authenticated or not libro.disponible:
        return redirect('detalle_libro', id=id)

    libro.disponible = False
    libro.prestado = True
    libro.save()
    libro.usuarios_prestamo.add(request.user)

    Prestamo.objects.create(
        usuario=request.user,
        libro=libro,
        fecha_fin=timezone.now() + timedelta(days=14),
        estado='RESERVADO',
    )

    return redirect('mis_prestamos')


def mis_prestamos(request):
    if not request.user.is_authenticated:
        return redirect('login')

    prestamos = Prestamo.objects.filter(usuario=request.user).select_related('libro')
    return render(request, 'Biblioteca_1/mis_prestamos.html', {'prestamos': prestamos})


def buscar(request):
    """Búsqueda de libros por título o autor"""
    query = request.GET.get('q', '')
    libros = []
    if query:
        libros = Libro.objects.filter(
            Q(titulo__icontains=query) | Q(autores__nombre__icontains=query)
        ).distinct()
    context = {'libros': libros, 'query': query}
    return render(request, 'Biblioteca_1/libros.html', context)
