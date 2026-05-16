from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/<int:id>/', views.detalle_libro, name='detalle_libro'),
    path('buscar/', views.buscar, name='buscar'),
]
