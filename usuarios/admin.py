from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefono', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {
            'fields': ('telefono', 'direccion', 'fecha_nacimiento')
        }),
    )
