from django.db import models
from django.conf import settings


class Genero(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Géneros'


class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True)
    anio = models.IntegerField(verbose_name='Año de publicación')
    stock = models.IntegerField(default=1)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.titulo

    def disponible(self):
        return self.stock > 0


class Prestamo(models.Model):
    socio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.socio.username} - {self.libro.titulo}"

    class Meta:
        ordering = ['-fecha_prestamo']
