from decimal import Decimal, InvalidOperation
from django import forms
from .models import Categoria, Classe, Processo, LancamentoEmpenho
from django.db.models import Sum

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css = 'form-select'
            if isinstance(field.widget, forms.SelectMultiple):
                css = 'form-select'
            field.widget.attrs['class'] = css


class CategoriaForm(BootstrapModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ativa']


class ClasseForm(BootstrapModelForm):
    class Meta:
        model = Classe
        fields = ['codigo', 'descricao', 'categorias', 'ativa']
        widgets = {'categorias': forms.SelectMultiple(attrs={'size': 6})}


from decimal import Decimal, InvalidOperation
from django import forms
from .models import Processo


class ProcessoForm(forms.ModelForm):
    valor_informado = forms.CharField(
        label="Valor informado",
        widget=forms.TextInput(attrs={
            "class": "form-control money",
            "placeholder": "0,00",
            "inputmode": "decimal",
        })
    )

    class Meta:
        model = Processo
        fields = [
            "numero",
            "ano_referencia",
            "valor_informado",
            "observacao",
            "ativo",
        ]

        widgets = {
            "numero": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "ano_referencia": forms.NumberInput(attrs={
                "class": "form-control",
            }),
            "observacao": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
            }),
            "ativo": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def clean_valor_informado(self):
        valor = self.cleaned_data.get("valor_informado", "0")

        valor = str(valor).strip()
        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

        try:
            valor = Decimal(valor)
        except InvalidOperation:
            raise forms.ValidationError("Informe um valor válido.")

        if valor < 0:
            raise forms.ValidationError("O valor informado não pode ser negativo.")

        return valor

class LancamentoEmpenhoForm(BootstrapModelForm):

    class Meta:
        model = LancamentoEmpenho

        fields = [
            "mes",
            "ano",
            "classe",
            "categoria",
            "processo",
            "valor_empenhado",
            "data_lancamento",
            "observacao",
            "conferido",
        ]

        widgets = {

            "mes": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "ano": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "classe": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "categoria": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "processo": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "valor_empenhado": forms.NumberInput(
                attrs={
                    "class": "form-control money",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "data_lancamento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "observacao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        processo = cleaned_data.get("processo")
        valor_empenhado = cleaned_data.get("valor_empenhado")

        if not processo or valor_empenhado is None:
            return cleaned_data

        if valor_empenhado < 0:
            self.add_error(
                "valor_empenhado",
                "O valor empenhado não pode ser negativo."
            )

            return cleaned_data

        total_empenhado = (
            LancamentoEmpenho.objects
            .filter(processo=processo)
            .exclude(pk=self.instance.pk)
            .aggregate(total=Sum("valor_empenhado"))["total"]
            or Decimal("0.00")
        )

        saldo_disponivel = (
            processo.valor_informado - total_empenhado
        )

        if valor_empenhado > saldo_disponivel:

            saldo_formatado = (
                f"R$ {saldo_disponivel:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            self.add_error(
                "valor_empenhado",
                (
                    "O valor informado é maior do que o saldo "
                    f"disponível para empenho. "
                    f"Saldo atual: {saldo_formatado}"
                )
            )

        return cleaned_data