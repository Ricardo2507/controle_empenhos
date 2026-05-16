from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .forms import (
    CategoriaForm,
    ClasseForm,
    ProcessoForm,
    LancamentoEmpenhoForm,
)

from .models import (
    Categoria,
    Classe,
    Processo,
    LancamentoEmpenho,
)


# =========================================================
# HELPERS
# =========================================================

MESES = [
    (1, "Janeiro"),
    (2, "Fevereiro"),
    (3, "Março"),
    (4, "Abril"),
    (5, "Maio"),
    (6, "Junho"),
    (7, "Julho"),
    (8, "Agosto"),
    (9, "Setembro"),
    (10, "Outubro"),
    (11, "Novembro"),
    (12, "Dezembro"),
]


def get_filtros_context():
    return {
        "anos": (
            LancamentoEmpenho.objects
            .values_list("ano", flat=True)
            .distinct()
            .order_by("-ano")
        ),

        "meses": MESES,

        "processos": (
            Processo.objects
            .all()
            .order_by("numero")
        ),

        "classes": (
            Classe.objects
            .all()
            .order_by("codigo")
        ),

        "categorias": (
            Categoria.objects
            .all()
            .order_by("nome")
        ),
    }

def filtrar_lancamentos(request):
    lancamentos = (
        LancamentoEmpenho.objects
        .select_related(
            "processo",
            "classe",
            "categoria",
        )
    )

    ano = request.GET.get("ano")
    mes = request.GET.get("mes")
    processo = request.GET.get("processo")
    classe = request.GET.get("classe")
    categoria = request.GET.get("categoria")

    if ano:
        lancamentos = lancamentos.filter(ano=ano)

    if mes:
        lancamentos = lancamentos.filter(mes=mes)

    if processo:
        lancamentos = lancamentos.filter(
            processo_id=processo
        )

    if classe:
        lancamentos = lancamentos.filter(
            classe_id=classe
        )

    if categoria:
        lancamentos = lancamentos.filter(
            categoria_id=categoria
        )

    return lancamentos


# =========================================================
# MIXINS
# =========================================================

class HtmxFormMixin:
    modal_title = ""
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["modal_title"] = self.modal_title
        context["form_action"] = self.request.path

        return context

    def form_valid(self, form):
        self.object = form.save()

        response = HttpResponse(status=204)
        response["HX-Redirect"] = self.get_success_url()

        return response


class HtmxDeleteMixin:
    success_message = ""

    def form_valid(self, form):
        self.object.delete()

        if self.success_message:
            messages.success(
                self.request,
                self.success_message
            )

        response = HttpResponse(status=204)
        response["HX-Redirect"] = self.get_success_url()

        return response


# =========================================================
# DASHBOARD
# =========================================================
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "empenhos/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lancamentos = filtrar_lancamentos(self.request)

        total_empenhado = (
            lancamentos.aggregate(
                total=Sum("valor_empenhado")
            )["total"]
            or Decimal("0.00")
        )

        processos_com_empenho = (
            LancamentoEmpenho.objects
            .values_list("processo_id", flat=True)
            .distinct()
        )

        total_informado = (
            Processo.objects
            .exclude(id__in=processos_com_empenho)
            .aggregate(total=Sum("valor_informado"))["total"]
            or Decimal("0.00")
        )

        resumo_financeiro_total = total_informado + total_empenhado

        total_processos = Processo.objects.count()

        top_classes = (
            lancamentos.values(
                "classe__codigo",
                "classe__descricao",
            )
            .annotate(total=Sum("valor_empenhado"))
            .order_by("-total")[:10]
        )

        top_categorias = (
            lancamentos.values(
                "categoria__nome",
            )
            .annotate(total=Sum("valor_empenhado"))
            .order_by("-total")[:10]
        )

        context.update(get_filtros_context())

        context["total_informado"] = total_informado
        context["total_empenhado"] = total_empenhado
        context["total_nao_empenhado"] = total_informado
        context["resumo_financeiro_total"] = resumo_financeiro_total

        context["saldo"] = total_informado
        context["saldo_total"] = total_informado

        context["total_processos"] = total_processos
        context["top_classes"] = top_classes
        context["top_categorias"] = top_categorias

        return context

# =========================================================
# CATEGORIAS
# =========================================================

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = "empenhos/categoria_list.html"
    context_object_name = "categorias"

    def get_queryset(self):
        return Categoria.objects.all().order_by("nome")


class CategoriaCreateView(
    LoginRequiredMixin,
    HtmxFormMixin,
    CreateView
):
    model = Categoria
    form_class = CategoriaForm
    template_name = "empenhos/partials/form_modal.html"
    success_url = reverse_lazy("categoria_list")
    modal_title = "Nova Categoria"


class CategoriaUpdateView(
    LoginRequiredMixin,
    HtmxFormMixin,
    UpdateView
):
    model = Categoria
    form_class = CategoriaForm
    template_name = "empenhos/partials/form_modal.html"
    success_url = reverse_lazy("categoria_list")
    modal_title = "Editar Categoria"


class CategoriaDeleteView(
    LoginRequiredMixin,
    HtmxDeleteMixin,
    DeleteView
):
    model = Categoria
    template_name = "empenhos/partials/confirm_delete.html"
    success_url = reverse_lazy("categoria_list")
    success_message = "Categoria removida com sucesso."


# =========================================================
# CLASSES
# =========================================================

class ClasseListView(LoginRequiredMixin, ListView):
    model = Classe
    template_name = "empenhos/classe_list.html"
    context_object_name = "classes"

    def get_queryset(self):
        return (
            Classe.objects
            .prefetch_related("categorias")
            .order_by("codigo")
        )


class ClasseCreateView(
    LoginRequiredMixin,
    HtmxFormMixin,
    CreateView
):
    model = Classe
    form_class = ClasseForm
    template_name = "empenhos/partials/form_modal.html"
    success_url = reverse_lazy("classe_list")
    modal_title = "Nova Classe"


class ClasseUpdateView(
    LoginRequiredMixin,
    HtmxFormMixin,
    UpdateView
):
    model = Classe
    form_class = ClasseForm
    template_name = "empenhos/partials/form_modal.html"
    success_url = reverse_lazy("classe_list")
    modal_title = "Editar Classe"


class ClasseDeleteView(
    LoginRequiredMixin,
    HtmxDeleteMixin,
    DeleteView
):
    model = Classe
    template_name = "empenhos/partials/confirm_delete.html"
    success_url = reverse_lazy("classe_list")
    success_message = "Classe removida com sucesso."


# =========================================================
# PROCESSOS
# =========================================================

class ProcessoListView(LoginRequiredMixin, ListView):
    model = Processo
    template_name = "empenhos/processo_list.html"
    context_object_name = "processos"

    def get_queryset(self):
        return (
            Processo.objects
            .all()
            .order_by("-criado_em")
        )


class ProcessoDetailView(LoginRequiredMixin, DetailView):
    model = Processo
    template_name = "empenhos/processo_detail.html"
    context_object_name = "processo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["lancamentos"] = (
            LancamentoEmpenho.objects
            .filter(processo=self.object)
            .select_related(
                "classe",
                "categoria",
            )
            .order_by("-data_lancamento")
        )

        return context


class ProcessoCreateView(
    LoginRequiredMixin,
    HtmxFormMixin,
    CreateView
):
    model = Processo
    form_class = ProcessoForm
    template_name = "empenhos/partials/form_modal.html"
    success_url = reverse_lazy("processo_list")
    modal_title = "Novo Processo"


class ProcessoUpdateView(
    LoginRequiredMixin,
    HtmxFormMixin,
    UpdateView
):
    model = Processo
    form_class = ProcessoForm
    template_name = "empenhos/partials/form_modal.html"
    success_url = reverse_lazy("processo_list")
    modal_title = "Editar Processo"


class ProcessoDeleteView(
    LoginRequiredMixin,
    HtmxDeleteMixin,
    DeleteView
):
    model = Processo
    template_name = "empenhos/partials/confirm_delete.html"
    success_url = reverse_lazy("processo_list")
    success_message = "Processo removido com sucesso."


# =========================================================
# LANÇAMENTOS
# =========================================================

class LancamentoListView(LoginRequiredMixin, ListView):
    model = LancamentoEmpenho
    template_name = "empenhos/lancamento_list.html"
    context_object_name = "lancamentos"

    def get_queryset(self):
        return (
            filtrar_lancamentos(self.request)
            .order_by("-data_lancamento")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(get_filtros_context())

        return context


class LancamentoCreateView(
    LoginRequiredMixin,
    HtmxFormMixin,
    CreateView
):
    model = LancamentoEmpenho
    form_class = LancamentoEmpenhoForm
    template_name = "empenhos/partials/form_modal.html"
    success_url = reverse_lazy("lancamento_list")
    modal_title = "Novo Lançamento"


class LancamentoUpdateView(
    LoginRequiredMixin,
    HtmxFormMixin,
    UpdateView
):
    model = LancamentoEmpenho
    form_class = LancamentoEmpenhoForm
    template_name = "empenhos/partials/form_modal.html"
    success_url = reverse_lazy("lancamento_list")
    modal_title = "Editar Lançamento"


class LancamentoDeleteView(
    LoginRequiredMixin,
    HtmxDeleteMixin,
    DeleteView
):
    model = LancamentoEmpenho
    template_name = "empenhos/partials/confirm_delete.html"
    success_url = reverse_lazy("lancamento_list")
    success_message = "Lançamento removido com sucesso."


# =========================================================
# CONSOLIDADO
# =========================================================

class ConsolidadoView(LoginRequiredMixin, TemplateView):
    template_name = "empenhos/consolidado.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lancamentos = filtrar_lancamentos(self.request)

        linhas = []

        for item in lancamentos.select_related("processo", "classe", "categoria"):
            informado = item.processo.valor_informado
            empenhado = item.valor_empenhado
            saldo = informado - item.processo.total_empenhado

            linhas.append({
                "classe": item.classe.codigo,
                "descricao": item.classe.descricao,
                "categoria": item.categoria.nome,
                "processo": item.processo.numero,
                "total_empenhado": empenhado,
                "total_informado": informado,
                "saldo": saldo,
            })

        context.update(get_filtros_context())
        context["lancamentos"] = lancamentos
        context["consolidado"] = linhas
        context["consolidados"] = linhas
        context["total_empenhado"] = (
            lancamentos.aggregate(total=Sum("valor_empenhado"))["total"]
            or Decimal("0.00")
        )

        return context



# =========================================================
# INFORMADO X EMPENHADO
# =========================================================

class InformadoEmpenhadoView(LoginRequiredMixin, TemplateView):
    template_name = "empenhos/informado_empenhado.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lancamentos = filtrar_lancamentos(self.request)

        grupos = {}

        for item in lancamentos.select_related("processo", "classe", "categoria"):
            chave = (item.processo_id, item.classe_id)

            if chave not in grupos:
                grupos[chave] = {
                    "classe": item.classe.codigo,
                    "processo": item.processo.numero,
                    "total_informado": item.processo.valor_informado,
                    "total_empenhado": Decimal("0.00"),
                }

            grupos[chave]["total_empenhado"] += item.valor_empenhado

        linhas = []

        for item in grupos.values():
            saldo = item["total_informado"] - item["total_empenhado"]

            percentual = Decimal("0.00")
            if item["total_informado"] > 0:
                percentual = (
                    item["total_empenhado"] / item["total_informado"]
                ) * 100

            situacao = "OK"

            if saldo < 0:
                situacao = "Excedido"
            elif saldo == 0:
                situacao = "Totalmente empenhado"
            elif item["total_empenhado"] > 0:
                situacao = "Parcial"

            linhas.append({
                "classe": item["classe"],
                "processo": item["processo"],
                "total_informado": item["total_informado"],
                "total_empenhado": item["total_empenhado"],
                "saldo": saldo,
                "percentual": percentual,
                "situacao": situacao,
            })

        context.update(get_filtros_context())

        context["informado_empenhado"] = linhas
        context["resumo"] = linhas

        context["total_informado"] = (
            Processo.objects.aggregate(total=Sum("valor_informado"))["total"]
            or Decimal("0.00")
        )

        context["total_empenhado"] = (
            lancamentos.aggregate(total=Sum("valor_empenhado"))["total"]
            or Decimal("0.00")
        )

        context["saldo_total"] = (
            context["total_informado"] - context["total_empenhado"]
        )

        return context



# =========================================================
# RELATÓRIO MENSAL
# =========================================================

class RelatorioMensalView(LoginRequiredMixin, TemplateView):
    template_name = "empenhos/relatorio_mensal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lancamentos = filtrar_lancamentos(self.request)

        grupos = {}

        for item in lancamentos.select_related("processo", "classe", "categoria"):
            chave = item.classe.id

            if chave not in grupos:
                grupos[chave] = {
                    "classe": item.classe.codigo,
                    "descricao": item.classe.descricao,
                    "processos": set(),
                    "total_mes": Decimal("0.00"),
                }

            grupos[chave]["processos"].add(item.processo.numero)
            grupos[chave]["total_mes"] += item.valor_empenhado

        linhas = []

        for linha in grupos.values():
            linhas.append({
                "classe": linha["classe"],
                "descricao": linha["descricao"],
                "processos": ", ".join(sorted(linha["processos"])),
                "total_mes": linha["total_mes"],
            })

        context.update(get_filtros_context())
        context["lancamentos"] = lancamentos
        context["relatorio"] = linhas
        context["relatorio_mensal"] = linhas

        context["total_empenhado"] = (
            lancamentos.aggregate(total=Sum("valor_empenhado"))["total"]
            or Decimal("0.00")
        )

        return context
    
