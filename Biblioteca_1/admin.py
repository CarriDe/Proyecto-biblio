from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.sites import NotRegistered

from .models import Autor, Categoria, Libro, Prestamo, Usuario


class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )


class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'disponible', 'validado', 'prestado', 'categoria', 'administrador_validar')
    list_filter = ('tipo', 'disponible', 'validado', 'prestado', 'categoria')
    search_fields = ('titulo', 'descripcion')
    filter_horizontal = ('autores', 'usuarios_prestamo')


class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion', 'devuelto')
    list_filter = ('devuelto',)
    search_fields = ('libro__titulo', 'usuario__username')


try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
