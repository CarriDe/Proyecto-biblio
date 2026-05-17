from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/<int:id>/', views.detalle_libro, name='detalle_libro'),
    path('libros/<int:id>/reservar/', views.reservar_libro, name='reservar_libro'),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('buscar/', views.buscar, name='buscar'),
]
