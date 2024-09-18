from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Perfil


class CustomUserAdmin(UserAdmin):
    # Campos que serão exibidos na página de listagem de usuários no admin
    list_display = ('username', 'email', 'is_cliente', 'is_hotel', 'is_staff')

    # Campos que serão exibidos ao editar um usuário no admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_cliente', 'is_hotel')}),
    )

    # Campos adicionais que serão utilizados ao criar um novo usuário no admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_cliente', 'is_hotel')}),
    )

    add_form = UserAdmin.add_form
    form = UserAdmin.form


admin.site.register(User, CustomUserAdmin)
admin.site.register(Perfil)
