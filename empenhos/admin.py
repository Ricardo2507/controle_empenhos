from django.contrib import admin

from .models import Categoria, Classe, Processo, LancamentoEmpenho


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "ativa",
    ]

    search_fields = [
        "nome",
    ]

    list_filter = [
        "ativa",
    ]


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "descricao",
        "ativa",
    ]

    search_fields = [
        "codigo",
        "descricao",
    ]

    list_filter = [
        "ativa",
        "categorias",
    ]

    filter_horizontal = [
        "categorias",
    ]


@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = [
        "numero",
        "ano_referencia",
        "valor_informado",
        "total_empenhado",
        "saldo_disponivel",
        "ativo",
    ]

    search_fields = [
        "numero",
        "observacao",
    ]

    list_filter = [
        "ativo",
        "ano_referencia",
    ]

    readonly_fields = [
        "total_empenhado",
        "saldo_disponivel",
        "criado_em",
        "atualizado_em",
    ]


@admin.register(LancamentoEmpenho)
class LancamentoEmpenhoAdmin(admin.ModelAdmin):
    list_display = [
        "mes",
        "ano",
        "processo",
        "classe",
        "categoria",
        "valor_empenhado",
        "data_lancamento",
        "conferido",
    ]

    search_fields = [
        "processo__numero",
        "classe__codigo",
        "classe__descricao",
        "categoria__nome",
        "observacao",
    ]

    list_filter = [
        "ano",
        "mes",
        "classe",
        "categoria",
        "conferido",
    ]

    autocomplete_fields = [
        "processo",
        "classe",
        "categoria",
    ]