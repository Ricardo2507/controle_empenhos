from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()


@register.filter
def brl(value):
    try:
        value = Decimal(value or 0)
    except (InvalidOperation, TypeError):
        value = Decimal('0')
    txt = f'{value:,.2f}'
    txt = txt.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {txt}'


@register.filter
def pct(value):
    try:
        value = Decimal(value or 0)
    except (InvalidOperation, TypeError):
        value = Decimal('0')
    return f'{value:.1f}%'.replace('.', ',')


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
