from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.sites import NotRegistered

from .models import Autor, Categoria, Libro, Prestamo, Usuario


class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )


class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido')
    search_fields = ('nombre', 'apellido')
    ordering = ('nombre', 'apellido')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'disponible', 'validado', 'prestado', 'categoria', 'administrador_validar')
    list_filter = ('tipo', 'disponible', 'validado', 'prestado', 'categoria')
    search_fields = ('titulo', 'descripcion', 'categoria__nombre', 'autores__nombre', 'administrador_validar__username')
    ordering = ('titulo',)
    date_hierarchy = 'fecha_publicacion'
    filter_horizontal = ('autores', 'usuarios_prestamo')


class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'libro__tipo', 'libro__categoria')
    search_fields = ('libro__titulo', 'libro__categoria__nombre', 'usuario__username', 'usuario__email')
    ordering = ('-fecha_inicio',)


try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
