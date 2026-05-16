from django.db import models
from django.db.models import Sum


class Categoria(models.Model):
    nome = models.CharField('Categoria', max_length=120, unique=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Classe(models.Model):
    codigo = models.PositiveIntegerField('Classe', unique=True)
    descricao = models.CharField('Descrição', max_length=180, blank=True)
    categorias = models.ManyToManyField(
        Categoria, related_name='classes', blank=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return str(self.codigo) if not self.descricao else f'{self.codigo} - {self.descricao}'


class Processo(models.Model):
    numero = models.CharField('Número do Processo',
                              max_length=120, unique=True)
    ano_referencia = models.IntegerField(
        default=2026
    )
    valor_informado = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )
    observacao = models.TextField('Observação', blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['numero']
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'

    def __str__(self):
        return self.numero

    @property
    def total_informado(self):
        return self.lancamentos.aggregate(total=Sum('valor_informado'))['total'] or 0

    @property
    def total_empenhado(self):
        return self.lancamentos.aggregate(total=Sum('valor_empenhado'))['total'] or 0

    @property
    def saldo(self):
        return self.total_informado - self.total_empenhado

    @property
    def total_empenhado(self):
        return self.lancamentos.aggregate(
            total=models.Sum('valor_empenhado')
        )['total'] or 0

    @property
    def saldo_disponivel(self):
        return self.valor_informado - self.total_empenhado


class LancamentoEmpenho(models.Model):
    MESES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
    ]

    mes = models.PositiveSmallIntegerField('Mês', choices=MESES)
    ano = models.PositiveIntegerField('Ano')
    classe = models.ForeignKey(
        Classe, on_delete=models.PROTECT, related_name='lancamentos')
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='lancamentos')
    processo = models.ForeignKey(
        Processo, on_delete=models.CASCADE, related_name='lancamentos')

    valor_empenhado = models.DecimalField(
        'Valor Empenhado', max_digits=14, decimal_places=2)
    data_lancamento = models.DateField(
        'Data do Lançamento', null=True, blank=True)
    observacao = models.CharField(
        'Usuário/Observação', max_length=255, blank=True)
    conferido = models.BooleanField('Conferido?', default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ano', '-mes', 'classe__codigo', 'processo__numero']
        verbose_name = 'Lançamento de Empenho'
        verbose_name_plural = 'Lançamentos de Empenhos'

    def __str__(self):
        return f'{self.get_mes_display()}/{self.ano} - {self.processo}'

    @property
    def percentual_empenhado(self):
        if not self.valor_informado:
            return 0
        return (self.valor_empenhado / self.valor_informado) * 100

    @property
    def situacao(self):
        if not self.valor_informado:
            return 'Sem valor informado'
        if self.saldo > 0:
            return 'Parcialmente empenhado'
        if self.saldo == 0:
            return 'Totalmente empenhado'
        return 'Empenhado acima do informado'
