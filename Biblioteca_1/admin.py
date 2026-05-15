from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.sites import NotRegistered

from .models import Libro, Usuario


class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )


try:
    admin.site.unregister(User)
except NotRegistered:
    pass
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Libro)
