from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        GESTOR = "GESTOR", "Gestor"
        OPERADOR = "OPERADOR", "Operador"
        CONSULTA = "CONSULTA", "Consulta"

    nome_completo = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nome completo",
    )

    setor = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Setor",
    )

    cargo = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Cargo",
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.OPERADOR,
        verbose_name="Tipo de usuário",
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone",
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em",
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        if self.nome_completo:
            return self.nome_completo
        return self.username