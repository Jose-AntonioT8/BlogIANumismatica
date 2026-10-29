import re
from datetime import date

MESES = (
    '',
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
)
TIPOS = ('Moneda', 'Billete', 'Medalla')


def fecha_es(value):
    return f'{value.day} de {MESES[value.month]} de {value.year}'


def excerpt(body):
    flat = re.sub(r'\s+', ' ', body).strip()
    if len(flat) <= 180:
        return flat
    return flat[:177].rstrip() + '…'


def paragraphs(body):
    blocks = []
    for block in re.split(r'\n\s*\n', body or ''):
        text = block.strip('\n')
        if text.strip():
            blocks.append(text.split('\n'))
    return blocks


def type_label(piece_type):
    return piece_type if piece_type in TIPOS else 'Sin clasificar'


def is_real_date(value):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value or ''):
        return False
    year, month, day = (int(part) for part in value.split('-'))
    try:
        date(year, month, day)
    except ValueError:
        return False
    return True
