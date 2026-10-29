"""Interfaz MCP de El Gabinete.

Expone los artículos de Django: listar, abrir uno y publicar otro.
No hay borradores. Crear usa la misma validación que el formulario web.
"""

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from herramientas import crear_articulo as guardar_articulo
from herramientas import listar_articulos as obtener_publicados
from herramientas import obtener_articulo as abrir_articulo


def _visible(llamada):
    try:
        return llamada()
    except ValueError as exc:
        raise ToolError(str(exc)) from exc

mcp = MCPServer(
    'El Gabinete',
    instructions=(
        'Blog local de numismática. Lista piezas, abre una por su identificador '
        'y publica otra con título, cuerpo, fecha AAAA-MM-DD y tipo '
        'Moneda, Billete o Medalla. Crear publica el artículo; no hay borradores.'
    ),
)


@mcp.tool()
def listar_articulos(tipo: str = '') -> list[dict]:
    """Lista las piezas del gabinete, de la más reciente a la más antigua.

    tipo puede quedar vacío o ser Todas, Moneda, Billete o Medalla.
    """
    return _visible(lambda: obtener_publicados(tipo))


@mcp.tool()
def obtener_articulo(identificador: str) -> dict:
    """Devuelve una pieza por su identificador, el mismo que aparece en la URL."""
    return _visible(lambda: abrir_articulo(identificador))


@mcp.tool()
def crear_articulo(titulo: str, cuerpo: str, fecha: str, tipo: str) -> dict:
    """Publica una pieza. fecha es AAAA-MM-DD. tipo es Moneda, Billete o Medalla."""
    return guardar_articulo(titulo, cuerpo, fecha, tipo)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('gabinete.asgi:application', host='127.0.0.1', port=8080)
