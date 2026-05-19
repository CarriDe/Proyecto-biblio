import json

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.sites import NotRegistered
from django.db.models import Count

from .models import Autor, Categoria, Libro, Prestamo, Usuario


class BibliotecaAdminSite(AdminSite):
    site_header = 'Biblioteca - Panel'
    site_title = 'Administración Biblioteca'
    index_title = 'Dashboard y estadísticas'
    site_url = '/'
    index_template = 'admin/custom_index.html'

    def each_context(self, request):
        context = super().each_context(request)
        context['dashboard_stats'] = self.get_dashboard_stats()
        context['chart_data'] = self.get_chart_data()
        context['quick_links'] = self.get_quick_links()
        return context

    def get_dashboard_stats(self):
        return {
            'libros_totales': Libro.objects.count(),
            'libros_disponibles': Libro.objects.filter(disponible=True).count(),
            'libros_prestados': Libro.objects.filter(prestado=True).count(),
            'prestamos_activos': Prestamo.objects.exclude(estado='DEVUELTO').count(),
            'usuarios_registrados': Usuario.objects.count(),
            'validaciones_pendientes': Libro.objects.filter(validado=False).count(),
        }

    def get_chart_data(self):
        tipos = list(Libro.objects.values('tipo').annotate(total=Count('id')).order_by('-total'))
        estados = list(Prestamo.objects.values('estado').annotate(total=Count('id')).order_by('-total'))
        return {
            'tipos': json.dumps([item['tipo'] for item in tipos], ensure_ascii=False),
            'tipos_totales': json.dumps([item['total'] for item in tipos]),
            'estados': json.dumps([item['estado'] for item in estados], ensure_ascii=False),
            'estados_totales': json.dumps([item['total'] for item in estados]),
        }

    def get_quick_links(self):
        return [
            {'label': 'Libros', 'url': 'admin:Biblioteca_1_libro_changelist'},
            {'label': 'Préstamos', 'url': 'admin:Biblioteca_1_prestamo_changelist'},
            {'label': 'Usuarios', 'url': 'admin:Biblioteca_1_usuario_changelist'},
            {'label': 'Autores', 'url': 'admin:Biblioteca_1_autor_changelist'},
            {'label': 'Categorías', 'url': 'admin:Biblioteca_1_categoria_changelist'},
        ]


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
    actions = ('marcar_como_disponible', 'marcar_como_prestado', 'validar_libros')

    @admin.action(description='Marcar libros como disponibles')
    def marcar_como_disponible(self, request, queryset):
        queryset.update(disponible=True, prestado=False)

    @admin.action(description='Marcar libros como prestados')
    def marcar_como_prestado(self, request, queryset):
        queryset.update(prestado=True, disponible=False)

    @admin.action(description='Validar libros seleccionados')
    def validar_libros(self, request, queryset):
        queryset.update(validado=True)


class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'libro__tipo', 'libro__categoria')
    search_fields = ('libro__titulo', 'libro__categoria__nombre', 'usuario__username', 'usuario__email')
    ordering = ('-fecha_inicio',)
    actions = ('marcar_devuelto',)

    @admin.action(description='Marcar préstamos como devueltos')
    def marcar_devuelto(self, request, queryset):
        queryset.update(estado='DEVUELTO')


custom_admin_site = BibliotecaAdminSite(name='admin')

try:
    admin.site.unregister(User)
except NotRegistered:
    pass

custom_admin_site.register(Usuario, UsuarioAdmin)
custom_admin_site.register(Autor, AutorAdmin)
custom_admin_site.register(Categoria, CategoriaAdmin)
custom_admin_site.register(Libro, LibroAdmin)
custom_admin_site.register(Prestamo, PrestamoAdmin)
