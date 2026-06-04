# Sistema de Biblioteca — Bootcamp Full Stack Python

Proyecto Django completo con autenticación, permisos y grupos.

## Instalación

```bash
# 1. Crear entorno virtual
python -m venv env

# 2. Activar entorno virtual
source env/bin/activate        # Mac/Linux
source env/Scripts/activate    # Windows Git Bash

# 3. Instalar dependencias
pip install -r requirements.txt

# 3.1 Instalar driver de PostgreSQL
pip install psycopg2-binary

# 4. Aplicar migraciones
python manage.py migrate

# 4.1 Poblar la bbdd
python manage.py shell < poblar_db.py

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Crear grupos desde el admin
# Entra a http://127.0.0.1:8000/admin/
# Authentication → Groups → Add Group
# Crear grupos: socio, bibliotecario
# Asignar permisos:
#   socio        → biblioteca | prestamo | Can add prestamo
#   bibliotecario → biblioteca | prestamo | Can view prestamo (y todos los de biblioteca)

# 7. Iniciar el servidor
python manage.py runserver
```

## URLs disponibles

| URL | Descripción | Acceso |
|-----|-------------|--------|
| `/` | Catálogo de libros | Todos |
| `/libro/<id>/` | Detalle de libro | Todos |
| `/libro/<id>/solicitar/` | Solicitar préstamo | Logueado |
| `/mis-prestamos/` | Ver mis préstamos | Logueado |
| `/prestamo/<id>/devolver/` | Devolver libro | Logueado (dueño) |
| `/panel/` | Panel bibliotecario | Grupo bibliotecario |
| `/usuarios/registro/` | Registro de socio | Público |
| `/usuarios/perfil/` | Mi perfil | Logueado |
| `/login/` | Iniciar sesión | Público |
| `/logout/` | Cerrar sesión | Logueado |
| `/admin/` | Panel administración | Staff |

## Modelos

- **CustomUser** (AbstractUser) → Socio con teléfono, dirección, fecha_nacimiento
- **Genero** → Nombre del género literario
- **Autor** → Nombre, apellido, nacionalidad
- **Libro** → Título, autor, género, año, stock, descripción
- **Prestamo** → Socio, libro, fecha_prestamo, fecha_devolucion, devuelto

## Grupos y permisos

| Grupo | Puede hacer |
|-------|-------------|
| socio | Ver libros, solicitar préstamo, ver sus préstamos |
| bibliotecario | Todo lo anterior + ver panel con todos los préstamos |
| admin/superuser | Acceso total |

## Migrar a PostgreSQL

Edita `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Luego instala el driver e instala:
```bash
pip install psycopg2-binary
python manage.py migrate
```
