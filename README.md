# Django Controle de Empenhos

Projeto recriado com base na planilha `controle_empenhos_corrigido_download_ok.xlsx`.

## Recursos

- Dashboard estilo PAINEL
- Lançamentos de empenhos com DataTables e botões
- Cadastros de Processos, Classes e Categorias em modais HTMX
- Relatório Consolidado por classe, categoria, processo e mês
- Informado x Empenhado com saldo e situação
- Relatório Mensal filtrável e imprimível
- Valores formatados em R$ no padrão brasileiro
- Importador opcional da planilha original

## Como rodar

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Importar a planilha original

Coloque a planilha na pasta raiz do projeto e rode:

```bash
python manage.py importar_planilha controle_empenhos_corrigido_download_ok.xlsx
```

Ou informe o caminho completo:

```bash
python manage.py importar_planilha E:\caminho\controle_empenhos_corrigido_download_ok.xlsx
```
