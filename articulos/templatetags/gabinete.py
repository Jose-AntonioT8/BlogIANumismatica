from django import template

from articulos.text import excerpt, fecha_es, paragraphs

register = template.Library()

register.filter('fecha_es', fecha_es)
register.filter('excerpt', excerpt)
register.filter('parrafos', paragraphs)
