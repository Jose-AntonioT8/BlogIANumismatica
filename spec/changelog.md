# Cambios de alcance

Si el comportamiento cambia, este fichero, el PRD y el resto de `spec/` se actualizan antes que el código.

## 2026-10-29 — Interfaz MCP

El ejemplo `servidor_mcp.py` deja de ser un blog de robótica con borradores. Pasa a ser la interfaz local de los artículos de Django: listar, abrir y publicar. Publicar usa el mismo formulario y los mismos mensajes que la web. No añade borradores, cuentas ni otra base de datos.

El servidor escucha en `http://127.0.0.1:8080/mcp`.

## 2026-10-29 — Django, Python y uv

La aplicación pasa de Node.js y un fichero JSON a Django con Python. Los artículos viven en SQLite, a través del ORM. Las páginas las pinta el servidor, así que portada, detalle, alta y filtros funcionan sin JavaScript.

No cambian las capacidades: listado, detalle, alta, validación, tipo de pieza y filtros. Cambia AC-9 (comando de arranque y dirección) y la frase de persistencia de AC-8: el artículo queda en `db.sqlite3`, no en `articles.json`.

Arranque: `uv sync`, `uv run python manage.py migrate` y `uv run python manage.py runserver 127.0.0.1:8080`. El entorno virtual es `.venv`, creado por uv. El puerto 8080 evita el 8000, que en esta máquina lo usa Docker.

## 2026-10-29 — Tipo de pieza

El alta gana un campo obligatorio, `tipo`, con tres valores: Moneda, Billete o Medalla. La portada puede mostrar todas las piezas o solo las de un tipo.

Motivo: un gabinete numismático mezcla soportes distintos y conviene separarlos sin abrir búsqueda, etiquetas libres ni categorías editables.

### Qué cambia en los criterios

- AC-1 y AC-3 pasan a mostrar también el tipo. El orden, el extracto, los párrafos y el aviso de pieza no encontrada no cambian.
- AC-5 pasa a exigir título, cuerpo, fecha y tipo.
- AC-6 pasa a rechazar el tipo vacío o distinto de los tres valores.
- Se añaden AC-10 (el tipo se guarda), AC-11 (filtro de la portada) y AC-12 (el tipo se ve en el detalle).
- AC-2, AC-4, AC-7, AC-8 y AC-9 siguen igual.

### Datos ya guardados

Un artículo antiguo sin `tipo` no se borra. En la portada y en el detalle se etiqueta como «Sin clasificar» y solo aparece con el filtro «Todas». Los ejemplos de `src/data/articles.json` quedan clasificados.
