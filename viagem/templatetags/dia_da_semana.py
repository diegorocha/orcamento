from datetime import date

from django import template

register = template.Library()


@register.filter
def dia_da_semana(value):
    nome_do_dia = {
        0: 'Seg',
        1: 'Ter',
        2: 'Qua',
        3: 'Qui',
        4: 'Sex',
        5: 'Sáb',
        6: 'Dom',
    }
    if isinstance(value, date):
        return nome_do_dia[value.weekday()]
    return value
