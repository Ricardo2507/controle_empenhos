from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),

    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/novo/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),

    path('classes/', views.ClasseListView.as_view(), name='classe_list'),
    path('classes/novo/', views.ClasseCreateView.as_view(), name='classe_create'),
    path('classes/<int:pk>/editar/', views.ClasseUpdateView.as_view(), name='classe_update'),
    path('classes/<int:pk>/excluir/', views.ClasseDeleteView.as_view(), name='classe_delete'),

    path('processos/', views.ProcessoListView.as_view(), name='processo_list'),
    path('processos/novo/', views.ProcessoCreateView.as_view(), name='processo_create'),
    path('processos/<int:pk>/editar/', views.ProcessoUpdateView.as_view(), name='processo_update'),
    path('processos/<int:pk>/excluir/', views.ProcessoDeleteView.as_view(), name='processo_delete'),
    path('processos/<int:pk>/', views.ProcessoDetailView.as_view(), name='processo_detail'),

    path('lancamentos/', views.LancamentoListView.as_view(), name='lancamento_list'),
    path('lancamentos/novo/', views.LancamentoCreateView.as_view(), name='lancamento_create'),
    path('lancamentos/<int:pk>/editar/', views.LancamentoUpdateView.as_view(), name='lancamento_update'),
    path('lancamentos/<int:pk>/excluir/', views.LancamentoDeleteView.as_view(), name='lancamento_delete'),

    path('relatorios/consolidado/', views.ConsolidadoView.as_view(), name='consolidado'),
    path('relatorios/informado-empenhado/', views.InformadoEmpenhadoView.as_view(), name='informado_empenhado'),
    path('relatorios/mensal/', views.RelatorioMensalView.as_view(), name='relatorio_mensal'),
]
