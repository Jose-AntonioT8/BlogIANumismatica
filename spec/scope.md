# Alcance

Coincide con el PRD. Si esta lista y el PRD discrepan, se corrigen juntos antes de programar.

## Dentro

- Portada con listado ordenado por fecha de publicación descendente y extracto calculado.
- Detalle de un artículo, con párrafos y texto sin interpretar HTML.
- Alta de artículo con título, cuerpo, fecha y tipo (Moneda, Billete o Medalla).
- Filtro de la portada por ese tipo, sin borrar artículos.
- Validación de título, cuerpo, fecha y tipo, con los mensajes del PRD.
- Persistencia en SQLite (`db.sqlite3`), con el modelo `Article` de Django.
- Cuatro artículos de ejemplo, con tipos distintos para poder probar el filtro.
- Estado vacío y artículo no encontrado.
- Arranque local documentado, con uv y el entorno virtual `.venv`.
- Páginas servidas por Django: listar, ver y crear.
- Interfaz MCP local sobre esos mismos artículos, con la misma validación.

## Fuera

- Autenticación, roles y moderación.
- Despliegue y dominio real.
- Comentarios, SEO avanzado y multidioma.
- Imágenes, búsqueda, etiquetas libres, categorías editables, edición y borrado.
- Editor enriquecido y varios autores identificados.

## Límite del autor

El autor es quien tiene el proceso en marcha. No hay forma de impedir que otra persona, en el mismo equipo y con acceso a ese puerto, publique un artículo. El MVP no intenta resolverlo.
