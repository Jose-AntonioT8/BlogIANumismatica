"""Acceso del MCP a los artículos de Django."""

import os


def asegurar_django():
    from django.apps import apps

    if apps.ready:
        return
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gabinete.settings')
    import django
    django.setup()


def listar_articulos(tipo: str = '') -> list[dict]:
    asegurar_django()
    from articulos.servicio import listar
    return listar(tipo)


def obtener_articulo(identificador: str) -> dict:
    asegurar_django()
    from articulos.servicio import obtener
    return obtener(identificador)


def crear_articulo(titulo: str, cuerpo: str, fecha: str, tipo: str) -> dict:
    asegurar_django()
    from articulos.servicio import crear
    return crear(titulo, cuerpo, fecha, tipo)
