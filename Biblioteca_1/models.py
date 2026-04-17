from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('ADMINISTRADOR', 'Administrador'),
        ('USUARIO', 'Usuario'),
        ('EMPLEADO', 'Empleado'),
    )
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='USUARIO')

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name or self.last_name else self.username


class Libro(models.Model):
    TIPO_CHOICES = (
        ('NOVELA', 'Novela'),
        ('ENSAYO', 'Ensayo'),
        ('CIENTIFICO', 'Científico'),
        ('INFANTIL', 'Infantil'),
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    disponible = models.BooleanField(default=True)
    validado = models.BooleanField(default=False)
    administrador_validar = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros_validados', limit_choices_to={'rol': 'ADMINISTRADOR'})
    prestado = models.BooleanField(default=False)
    creado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='libros_creados', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    usuarios_prestamo = models.ManyToManyField(Usuario, related_name='libros_prestados', blank=True, limit_choices_to={'rol': 'USUARIO'})

    def __str__(self):
        return self.titulo

