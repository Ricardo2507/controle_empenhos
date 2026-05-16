from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    list_display = [
        "username",
        "nome_completo",
        "email",
        "tipo",
        "setor",
        "cargo",
        "is_active",
        "is_staff",
    ]

    list_filter = [
        "tipo",
        "setor",
        "is_active",
        "is_staff",
        "is_superuser",
    ]

    search_fields = [
        "username",
        "nome_completo",
        "email",
        "setor",
        "cargo",
    ]

    ordering = [
        "username",
    ]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Dados complementares",
            {
                "fields": (
                    "nome_completo",
                    "setor",
                    "cargo",
                    "tipo",
                    "telefone",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Dados complementares",
            {
                "fields": (
                    "nome_completo",
                    "email",
                    "setor",
                    "cargo",
                    "tipo",
                    "telefone",
                )
            },
        ),
    )