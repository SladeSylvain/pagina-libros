<div align="center">

# 📚 Biblioteca Project

**Sistema de gestión bibliotecaria** construido con Django 5 y PostgreSQL.  
Proyecto de aprendizaje enfocado en consultas ORM avanzadas, autenticación por roles y optimización de rendimiento.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=flat-square&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Status-En%20desarrollo-yellow?style=flat-square)

</div>

---

## 📌 Sobre el proyecto

Aplicación web que simula el flujo real de una biblioteca: catálogo navegable, sistema de préstamos con control de stock, y panel de administración exclusivo para bibliotecarios. El foco del proyecto está en **dominar el ORM de Django** — desde consultas básicas hasta agregaciones, JOINs implícitos y eliminación del problema N+1.

---

## ✨ Funcionalidades

| Feature | Detalle |
|---|---|
| 🔍 **Catálogo con triple filtro** | Búsqueda simultánea por título, género y apellido del autor |
| 📖 **Sistema de préstamos** | Solicitar y devolver libros con control de stock en tiempo real |
| 👤 **Autenticación y roles** | Registro, login y dos grupos: `socio` y `bibliotecario` |
| 🛡️ **Control de permisos** | Decoradores `@login_required` y `@permission_required` por vista |
| 📊 **Panel de bibliotecario** | Métricas de préstamos activos e inventario total |
| 🗃️ **Admin personalizado** | Modelos registrados y configurados en `django.contrib.admin` |

---

## 🧩 Modelos de datos

```
Genero ──────────────────────────────┐
                                     │ FK (SET_NULL)
Autor ──── nombre, apellido,         │
           nacionalidad        Libro ─┼── titulo, anio, stock, descripcion
                                     │
                               Prestamo ── socio (FK User), libro (FK),
                                           fecha_prestamo, fecha_devolucion, devuelto
```

---

## 🧠 Aprendizajes técnicos clave

### 1 — Filtros encadenados navegando ForeignKey

La vista `lista_libros` combina tres filtros opcionales en una sola queryset. El lookup `autor__apellido__icontains` navega la FK de `Libro → Autor` y Django genera el JOIN automáticamente.

```python
# views.py
libros = Libro.objects.select_related('autor', 'genero').all()

if titulo_busq:
    libros = libros.filter(titulo__icontains=titulo_busq)

if genero_id:
    libros = libros.filter(genero__id=genero_id)

if autor_busq:
    libros = libros.filter(autor__apellido__icontains=autor_busq)  # ← doble underscore = JOIN
```

> **Flujo de desarrollo:** primero verificar la consulta en `python manage.py shell`, confirmar resultados, y recién entonces llevarla a la vista. Evita errores silenciosos.

---

### 2 — Eliminación del problema N+1 con `select_related`

Sin `select_related`, Django ejecuta una query separada por cada libro para obtener el autor → **N+1 queries**.

```python
# ❌ Antes — 1 query para libros + N queries para autores
libros = Libro.objects.all()
for libro in libros:
    print(libro.autor.nombre)  # query extra en cada iteración

# ✅ Después — 1 solo JOIN, sin importar cuántos libros haya
libros = Libro.objects.select_related('autor', 'genero').all()
for libro in libros:
    print(libro.autor.nombre)  # dato ya cargado, 0 queries extra
```

---

### 3 — Consultas de agregación con `annotate` y `Count`

```python
from django.db.models import Count

# Libros por género, de mayor a menor
Genero.objects.annotate(total=Count('libro')).order_by('-total')

# Resultado:
# Terror → 8 libros
# Ciencia Ficción → 5 libros
# ...
```

`annotate()` agrega una columna calculada a cada objeto del queryset. Se ejecuta como un `GROUP BY` en SQL.

---

### 4 — Consultas ORM practicadas en el shell

```python
# Libros del género Terror con nombre completo del autor
Libro.objects.filter(
    genero__nombre__iexact='Terror'
).select_related('autor')

# Libros con stock mayor a 2
Libro.objects.filter(stock__gt=2).count()

# Los 3 libros más antiguos
Libro.objects.order_by('anio')[:3]

# Libros de autores chilenos con stock disponible
Libro.objects.filter(
    autor__nacionalidad__iexact='chilena',
    stock__gt=0
).select_related('autor')

# Cantidad de libros por género (mayor a menor)
Genero.objects.annotate(total=Count('libro')).order_by('-total')
```

---

## ⚙️ Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/biblioteca_project.git
cd biblioteca_project

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar PostgreSQL en config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca_db',
        'USER': '<tu_usuario>',
        'PASSWORD': '<tu_password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 4. Aplicar migraciones y poblar datos de prueba
python manage.py migrate
python poblar_db.py

# 5. Levantar el servidor
python manage.py runserver
```

---

## 🗂️ Estructura

```
biblioteca_project/
├── biblioteca/              # App principal
│   ├── models.py            # Genero, Autor, Libro, Prestamo
│   ├── views.py             # Vistas con filtros, préstamos y panel
│   ├── urls.py
│   └── templates/biblioteca/
├── usuarios/                # Registro, login y perfil
├── config/                  # settings.py y urls raíz
├── poblar_db.py             # Script de datos de prueba
└── requirements.txt
```

---

## 👤 Autor

**Slade Sylvain**  
Cloud Engineer · Junior Full Stack Developer  
AWS Cloud Practitioner | Python · Django · PostgreSQL · AWS

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)]([https://linkedin.com/in/tu-usuario](https://www.linkedin.com/in/alexandercarvajalp/))
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat-square&logo=github)](https://github.com/SladeSylvain)

