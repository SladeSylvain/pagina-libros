from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Libro, Genero, Prestamo, Autor


def lista_libros(request):
    libros = Libro.objects.select_related('autor', 'genero').all()

    titulo_busq = request.GET.get('titulo', '')
    genero_id   = request.GET.get('genero', '')
    autor_busq  = request.GET.get('autor', '')      # ← nuevo

    if titulo_busq:
        libros = libros.filter(titulo__icontains=titulo_busq)

    if genero_id:
        libros = libros.filter(genero__id=genero_id)

    if autor_busq:                                              # ← nuevo bloque
        libros = libros.filter(autor__apellido__icontains=autor_busq)

    contexto = {
        'libros':      libros,
        'titulo_busq': titulo_busq,
        'genero_id':   genero_id,
        'autor_busq':  autor_busq,    # ← necesario para que el input recuerde el valor
        'generos':     Genero.objects.all(),
    }
    return render(request, 'biblioteca/lista_libros.html', contexto)


def detalle_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    return render(request, 'biblioteca/detalle_libro.html', {'libro': libro})


@login_required
def solicitar_prestamo(request, pk):
    libro = get_object_or_404(Libro, pk=pk)

    if not libro.disponible():
        messages.error(request, 'Este libro no tiene stock disponible.')
        return redirect('detalle_libro', pk=pk)

    # Verificar que no tenga ya un préstamo activo de este libro
    prestamo_activo = Prestamo.objects.filter(
        socio=request.user,
        libro=libro,
        devuelto=False
    ).exists()

    if prestamo_activo:
        messages.warning(request, 'Ya tienes este libro en préstamo.')
        return redirect('detalle_libro', pk=pk)

    if request.method == 'POST':
        Prestamo.objects.create(socio=request.user, libro=libro)
        libro.stock -= 1
        libro.save()
        messages.success(request, f'Préstamo de "{libro.titulo}" registrado correctamente.')
        return redirect('mis_prestamos')

    return render(request, 'biblioteca/confirmar_prestamo.html', {'libro': libro})


@login_required
def mis_prestamos(request):
    prestamos = Prestamo.objects.filter(
        socio=request.user
    ).select_related('libro', 'libro__autor')
    return render(request, 'biblioteca/mis_prestamos.html', {'prestamos': prestamos})


@login_required
def devolver_libro(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk, socio=request.user)

    if prestamo.devuelto:
        messages.info(request, 'Este libro ya fue devuelto.')
        return redirect('mis_prestamos')

    if request.method == 'POST':
        from django.utils import timezone
        prestamo.devuelto = True
        prestamo.fecha_devolucion = timezone.now().date()
        prestamo.save()
        prestamo.libro.stock += 1
        prestamo.libro.save()
        messages.success(request, f'"{prestamo.libro.titulo}" devuelto correctamente.')
        return redirect('mis_prestamos')

    return render(request, 'biblioteca/confirmar_devolucion.html', {'prestamo': prestamo})


@login_required
@permission_required('biblioteca.view_prestamo', raise_exception=True)
def panel_bibliotecario(request):
    prestamos_activos = Prestamo.objects.filter(
        devuelto=False
    ).select_related('socio', 'libro', 'libro__autor').order_by('-fecha_prestamo')

    total_libros = Libro.objects.count()
    total_prestamos = Prestamo.objects.count()
    prestamos_pendientes = prestamos_activos.count()

    return render(request, 'biblioteca/panel_bibliotecario.html', {
        'prestamos_activos': prestamos_activos,
        'total_libros': total_libros,
        'total_prestamos': total_prestamos,
        'prestamos_pendientes': prestamos_pendientes,
    })