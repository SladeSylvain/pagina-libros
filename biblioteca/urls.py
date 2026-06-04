from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('libro/<int:pk>/', views.detalle_libro, name='detalle_libro'),
    path('libro/<int:pk>/solicitar/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('prestamo/<int:pk>/devolver/', views.devolver_libro, name='devolver_libro'),
    path('panel/', views.panel_bibliotecario, name='panel_bibliotecario'),
]
