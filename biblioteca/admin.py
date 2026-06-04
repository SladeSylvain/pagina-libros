from django.contrib import admin
from .models import Genero, Autor, Libro, Prestamo


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'nacionalidad')
    search_fields = ('nombre', 'apellido')


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'genero', 'anio', 'stock')
    search_fields = ('titulo', 'autor__nombre', 'autor__apellido')
    list_filter = ('genero', 'anio')
    list_editable = ('stock',)


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('id', 'socio', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'devuelto')
    list_filter = ('devuelto',)
    search_fields = ('socio__username', 'libro__titulo')
    list_editable = ('devuelto',)
