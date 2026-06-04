# 📚 Biblioteca Project

Aplicación web construida con **Django 5** y **PostgreSQL** como ejercicio de aprendizaje práctico.  
Simula un sistema de biblioteca con catálogo, préstamos y panel de administración para bibliotecarios.

---

## 🚀 Stack

| Tecnología | Uso |
|---|---|
| Python / Django 5 | Backend y lógica de negocio |
| PostgreSQL | Base de datos relacional |
| Django ORM | Consultas y relaciones entre modelos |
| Django Auth | Autenticación, permisos y decoradores |
| HTML / Templates | Frontend con herencia de plantillas |

---

## 🗂️ Estructura del proyecto

```
biblioteca_project/
├── biblioteca/          # App principal
│   ├── models.py        # Genero, Autor, Libro, Prestamo
│   ├── views.py         # Vistas con filtros, préstamos y panel
│   └── templates/
├── usuarios/            # App de registro y perfil
├── config/              # Settings, URLs raíz
├── poblar_db.py         # Script para poblar datos de prueba
└── requirements.txt
```

---

## 🧩 Modelos

```python
Genero      → nombre
Autor       → nombre, apellido, nacionalidad
Libro       → titulo, autor (FK), genero (FK), anio, stock, descripcion
Prestamo    → socio (FK User), libro (FK), fecha_prestamo, fecha_devolucion, devuelto
```

Las relaciones entre modelos usan `ForeignKey` con `on_delete=CASCADE` y `SET_NULL` según el caso.

---

## 🔍 Funcionalidades

- **Catálogo con triple filtro** — búsqueda por título, género y apellido del autor
- **Detalle de libro** — información completa y disponibilidad de stock
- **Sistema de préstamos** — solicitar y devolver libros (requiere login)
- **Panel del bibliotecario** — vista de préstamos activos con estadísticas (requiere permiso `view_prestamo`)
- **Mis préstamos** — historial del usuario autenticado
- **Registro y perfil** — app de usuarios separada

---

## 🧠 Ejercicio 1 — Filtro por apellido del autor

**Objetivo:** agregar un tercer parámetro de búsqueda al catálogo (`?autor=`) navegando la relación FK entre `Libro` y `Autor`.

### Paso 1 — Verificar la consulta en el shell antes de tocar las vistas

```python
python manage.py shell

from biblioteca.models import Libro
Libro.objects.filter(autor__apellido__icontains='King').select_related('autor')
```

Si retorna libros → la consulta funciona. Recién ahí se pasa a la vista.

### Paso 2 — `views.py`

```python
autor_busq = request.GET.get('autor', '')

if autor_busq:
    libros = libros.filter(autor__apellido__icontains=autor_busq)

contexto = {
    ...
    'autor_busq': autor_busq,   # necesario para que el input recuerde el valor
}
```

**Concepto clave:** `autor__apellido__icontains` navega la FK de `Libro` hacia `Autor` en una sola consulta. Django genera el JOIN automáticamente.

### Paso 3 — Template `lista_libros.html`

```html
<input type="text" name="autor" value="{{ autor_busq }}" placeholder="Apellido del autor">
```

El `value="{{ autor_busq }}"` mantiene el texto escrito al hacer submit del formulario.

---

## 📊 Ejercicio 2 — Consultas ORM en el shell

Práctica de consultas complejas con el ORM de Django usando `Count`, `Sum`, filtros encadenados y `select_related`.

```python
python manage.py shell

from biblioteca.models import Libro, Autor, Genero, Prestamo
from django.db.models import Count, Sum
```

### Consulta 1 — Libros del género Terror con nombre completo del autor

```python
libros_terror = Libro.objects.filter(
    genero__nombre__iexact='Terror'
).select_related('autor')

for libro in libros_terror:
    print(f"{libro.titulo} — {libro.autor.nombre} {libro.autor.apellido}")
```

### Consulta 2 — Cantidad de libros con stock mayor a 2

```python
total = Libro.objects.filter(stock__gt=2).count()
print(f"Libros con stock > 2: {total}")
```

### Consulta 3 — Los 3 libros más antiguos

```python
libros_antiguos = Libro.objects.order_by('anio')[:3]
for libro in libros_antiguos:
    print(f"{libro.anio} — {libro.titulo}")
```

### Consulta 4 — Libros de autores chilenos con stock disponible

```python
libros_cl = Libro.objects.filter(
    autor__nacionalidad__iexact='chilena',
    stock__gt=0
).select_related('autor')

for libro in libros_cl:
    print(f"{libro.titulo} — stock: {libro.stock}")
```

### Consulta 5 — Cantidad de libros por género (de mayor a menor)

```python
conteo = Genero.objects.annotate(
    total=Count('libro')
).order_by('-total')

for g in conteo:
    print(f"{g.nombre}: {g.total} libros")
```

**Conceptos aplicados:** `annotate()`, `Count()`, `order_by()` con `-` para descendente, `select_related()` para evitar N+1 queries, lookups encadenados sobre FK (`autor__apellido__icontains`).

---

## ⚙️ Setup local

```bash
git clone <repo>
cd biblioteca_project
pip install -r requirements.txt

# Configurar PostgreSQL en config/settings.py → DATABASES
python manage.py migrate
python poblar_db.py   # carga datos de prueba
python manage.py runserver
```

---

## 👤 Autor

**Slade Sylvain** — Cloud Engineer & Junior Full Stack Developer  
AWS Cloud Practitioner | Python · Django · PostgreSQL · AWS
