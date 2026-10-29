# El Gabinete

Blog local de numismática, hecho con Django. El alcance está cerrado en [PRD.md](PRD.md) y en [spec/](spec/).

## Ejecutar en local

Requisito: [uv](https://docs.astral.sh/uv/) y conexión la primera vez, para crear el entorno virtual `.venv` e instalar Django. uv usa Python 3.13.

```powershell
cd blog
uv sync
uv run python manage.py migrate
uv run python manage.py runserver 127.0.0.1:8080
```

Abrir [http://127.0.0.1:8080](http://127.0.0.1:8080). Si ese puerto está ocupado, cambia el número en el comando y en el navegador.

`migrate` crea `db.sqlite3` y carga los cuatro artículos de ejemplo.

Comprobaciones automáticas:

```powershell
uv run python manage.py test
```

Los tests usan una base temporal. No modifican `db.sqlite3`.

Interfaz MCP de los mismos artículos, en otro proceso:

```powershell
uv run python servidor_mcp.py
```

Queda en [http://127.0.0.1:8001/mcp](http://127.0.0.1:8001/mcp). Herramientas: `listar_articulos`, `obtener_articulo` y `crear_articulo`. Crear publica la pieza; no hay borradores.

## Mapa de ficheros

| Fichero | Qué contiene |
| --- | --- |
| `briefing.md` | Intención, usuarios y decisiones de producto. |
| `PRD.md` | Contrato: alcance, datos, mensajes y criterios. |
| `spec/vision.md` | Para quién es el blog y qué cuenta como éxito. |
| `spec/scope.md` | Qué entra y qué queda fuera. |
| `spec/acceptance_criteria.md` | Lista verificable y en qué fichero se implementa cada criterio. |
| `spec/changelog.md` | Cambios de alcance, spec antes que código. |
| `pyproject.toml` | Proyecto Python y dependencia Django. uv crea `.venv`. |
| `manage.py` | Punto de entrada de Django. |
| `gabinete/settings.py` | Configuración local: SQLite, español, estáticos. |
| `gabinete/urls.py` | Incluye las rutas de artículos. |
| `articulos/models.py` | Modelo `Article`, orden y slug. |
| `articulos/forms.py` | Alta y mensajes de validación. |
| `articulos/servicio.py` | Listar, abrir y crear artículos para la interfaz MCP. |
| `herramientas.py` | Arranca Django y llama a ese servicio. |
| `servidor_mcp.py` | Servidor MCP en el puerto 8001. |
| `articulos/views.py` | Portada, detalle, alta y 404. |
| `articulos/text.py` | Fecha en español, extracto y párrafos. |
| `articulos/seed_data.py` | Los cuatro artículos de ejemplo. |
| `articulos/tests.py` | Criterios de aceptación automáticos. |
| `articulos/templates/articulos/` | Portada, detalle, alta y pieza no encontrada. |
| `static/styles.css` | Presentación. |
| `db.sqlite3` | Artículos guardados. Lo crea `migrate`. No se versiona. |

## Dónde se implementa cada criterio

| Criterio | Dónde |
| --- | --- |
| AC-1 Portada y orden | `views.index`, `models.py`, `index.html`, `text.py` |
| AC-2 Estado vacío | `index.html` |
| AC-3 Detalle | `views.detail`, `detail.html`, `text.py` |
| AC-4 No encontrado | `views.detail`, `missing.html`, respuesta 404 |
| AC-5 Alta válida | `forms.py`, `views.create`, `create.html` |
| AC-6 Validación | `forms.py`, `create.html` |
| AC-7 Visible en la portada | `models.py`, `index.html` |
| AC-8 Persistencia | `models.py`, `db.sqlite3` |
| AC-9 Arranque local | `pyproject.toml`, `manage.py`, este README |
| AC-10 Tipo guardado | `forms.py`, `models.py` |
| AC-11 Filtro por tipo | `views.index`, `index.html` |
| AC-12 Tipo en el detalle | `detail.html`, `text.py` |

Los cambios de alcance están en [spec/changelog.md](spec/changelog.md).

## Flujo

El navegador pide páginas a Django. Las vistas leen o escriben artículos en SQLite con el modelo `Article`. No hay autenticación: publica quien usa el servidor local, tal como fija el PRD.
