# Criterios de aceptación

Lista verificable del MVP. El texto de cada criterio coincide con el PRD.
Si se cambia un criterio, se cambian este fichero y el PRD antes de tocar el código.

La columna «Dónde» responde en qué parte del repositorio se implementa.

## AC-1 — Portada

Dado que existen artículos guardados,
cuando abro la portada,
entonces veo cada uno con su título, su tipo, su fecha de publicación en español y el extracto definido en el PRD, ordenados de la fecha más reciente a la más antigua. Si dos fechas coinciden, va antes el de `createdAt` más reciente.

Dónde: `articulos/views.py` (`index`), `articulos/models.py` (orden), `articulos/templates/articulos/index.html`, `articulos/text.py` (fecha y extracto).

## AC-2 — Estado vacío

Dado que no hay ningún artículo,
cuando abro la portada,
entonces veo «El gabinete está vacío», «Todavía no hay piezas catalogadas.» y el enlace «Catalogar la primera pieza».

Dónde: `articulos/templates/articulos/index.html`.

## AC-3 — Detalle

Dado que existe un artículo,
cuando lo abro desde la portada,
entonces veo el título, el tipo, la fecha y el cuerpo completo. Una línea en blanco empieza otro párrafo. Un salto simple se conserva. El HTML escrito en el cuerpo se muestra como texto.

Dónde: `articulos/views.py` (`detail`), `articulos/templates/articulos/detail.html`, `articulos/text.py`.

## AC-4 — No encontrado

Dado un identificador ausente o desconocido,
cuando abro el detalle,
entonces veo «Pieza no encontrada», «Ese artículo no está en el gabinete.» y «Volver al listado». La respuesta es HTTP 404.

Dónde: `articulos/views.py`, `articulos/templates/articulos/missing.html`.

## AC-5 — Alta válida

Dado el formulario de alta,
cuando envío título, cuerpo, fecha y tipo válidos,
entonces se crea el artículo, queda guardado con ese tipo y se abre su página de detalle.

Dónde: `articulos/forms.py`, `articulos/views.py` (`create`), `articulos/templates/articulos/create.html`.

## AC-6 — Alta inválida

Dado el formulario de alta,
cuando falta el título, el cuerpo, la fecha o el tipo, la fecha no es un día real `AAAA-MM-DD`, el tipo no es Moneda, Billete ni Medalla, el título supera 120 caracteres o el cuerpo supera 20000,
entonces no se crea ningún artículo y aparece el mensaje de ese campo definido en el PRD.

Dónde: `articulos/forms.py`, `articulos/templates/articulos/create.html`.

## AC-7 — El alta se ve en la portada

Dado un artículo recién creado,
cuando vuelvo a la portada,
entonces aparece con su título y en la posición que le corresponde por fecha.

Dónde: `articulos/models.py`, `articulos/templates/articulos/index.html`.

## AC-8 — Persistencia

Dado un artículo creado,
cuando se reinicia el servidor,
entonces ese artículo sigue en SQLite y en el listado.

Dónde: `articulos/models.py`, `db.sqlite3`.

## AC-9 — Ejecución local

Dado un equipo con uv y Python 3.12 o 3.13,
cuando en la carpeta `blog` ejecuto `uv sync`, `uv run python manage.py migrate` y `uv run python manage.py runserver 127.0.0.1:8080`,
entonces el blog responde en `http://127.0.0.1:8080`.

Dónde: `pyproject.toml`, `manage.py`, `gabinete/settings.py`, `README.md`.

## AC-10 — Tipo guardado

Dado el formulario de alta,
cuando el tipo va vacío o no es Moneda, Billete ni Medalla,
entonces no se guarda nada y veo el mensaje del PRD.
Cuando el tipo es uno de esos tres,
entonces el artículo guardado lleva exactamente ese valor.

Dónde: `articulos/forms.py`, `articulos/models.py`, `articulos/templates/articulos/create.html`.

## AC-11 — Filtro de la portada

Dado que hay artículos,
cuando uso los controles Todas, Moneda, Billete y Medalla,
entonces la portada solo muestra las piezas de ese tipo, sin borrar el resto.
Si el tipo elegido no tiene piezas, veo «No hay piezas de este tipo.»
El estado vacío global solo aparece cuando no hay ningún artículo, y en ese caso no se muestran los filtros.
Un artículo sin tipo se etiqueta «Sin clasificar», entra en Todas y no entra en los otros tres filtros.

Dónde: `articulos/views.py`, `articulos/templates/articulos/index.html`, `articulos/text.py`.

## AC-12 — Tipo en el detalle

Dado un artículo con tipo,
cuando abro su detalle,
entonces el tipo se lee junto al título y la fecha. Si no tiene tipo, se lee «Sin clasificar».

Dónde: `articulos/templates/articulos/detail.html`, `articulos/text.py`.

## Cómo se comprueba

- `uv run python manage.py test` ejercita AC-1 (orden y empate), AC-2, AC-4, AC-5, AC-6, AC-7, AC-8, AC-10, AC-11 y AC-12.
- El navegador comprueba los textos de AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-11 y AC-12.
