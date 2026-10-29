# PRD — El Gabinete (blog de numismática)

Versión: MVP 1.2
Estado: acuerdo de producto para implementar y verificar en local.
El cambio 1.1 (tipo de pieza) está registrado en `spec/changelog.md`.

Este documento es el contrato. `spec/` lo detalla sin cambiarlo. Si el alcance cambia, se edita primero aquí y en `spec/`, y después el código.

## 1. Resumen

El Gabinete es un blog local de numismática. Muestra un listado de artículos, permite leer uno entero, filtrar por tipo de pieza y crear otro con título, cuerpo, fecha de publicación y tipo. Los datos viven en un fichero del proyecto. No hay cuentas, comentarios ni despliegue público.

## 2. Problema y usuarios

Hace falta un sitio pequeño para ordenar lecturas numismáticas y enseñar el flujo portada → detalle → alta, sin montar un CMS.

- Lector: consulta la portada y el detalle.
- Autor local: rellena el formulario de alta. Es la misma persona que arranca el servidor. No inicia sesión.

## 3. Glosario

| Término | Significado en este producto |
| --- | --- |
| Artículo | Una pieza publicada: título, cuerpo, fecha de publicación, tipo e identificador. |
| Tipo | Clase cerrada de la pieza: Moneda, Billete o Medalla. |
| Portada | La página inicial. Lista los artículos. |
| Detalle | La página de un solo artículo. |
| Alta | El formulario que crea un artículo. |
| Fecha de publicación | Día elegido en el alta, con formato `AAAA-MM-DD`. No es la hora del sistema. |
| Extracto | Texto calculado al mostrar la portada. No se pide en el formulario ni se guarda aparte. |
| `createdAt` | Instante interno de creación, en ISO 8601. Desempata el orden si dos artículos comparten fecha. No se muestra. |

## 4. Historias

1. Como lector, quiero ver los artículos en la portada con título, fecha y un extracto, para elegir qué leer.
2. Como lector, quiero abrir un artículo y leer el cuerpo completo.
3. Como autor local, quiero guardar un artículo con título, cuerpo, fecha y tipo, y verlo publicado.
3b. Como lector, quiero filtrar la portada por Moneda, Billete o Medalla.
4. Como autor local, quiero que un alta incompleta no se guarde y me diga qué falta.
5. Como autor local, quiero que lo publicado siga disponible al reiniciar la aplicación.

## 5. Alcance del MVP

Dentro:

- Portada con el listado de artículos.
- Página de detalle de un artículo.
- Alta con título, cuerpo, fecha de publicación y tipo de pieza.
- Filtro de la portada por tipo: Todas, Moneda, Billete o Medalla.
- Persistencia en SQLite local, mediante el ORM de Django.
- Ejecución en el propio equipo, documentada en el README.
- Artículos de ejemplo para que la primera visita no esté vacía.
- Estado vacío de la portada si no queda ningún artículo.
- Aviso si se pide un detalle que no existe.

Fuera:

- Autenticación, registro, roles y moderación.
- Despliegue, dominio, HTTPS público y copias en la nube.
- Comentarios, valoraciones y formularios de contacto.
- SEO avanzado: sitemap, datos estructurados, Open Graph, metas por artículo.
- Multidioma y traducción de la interfaz.
- Imágenes, galerías y fichas de subasta.
- Búsqueda, etiquetas libres, categorías editables y edición o borrado de artículos. El tipo cerrado (Moneda, Billete, Medalla) sí forma parte del MVP 1.1.
- Editor enriquecido. El cuerpo es texto plano.
- Varios autores identificados.

## 6. Comportamiento

### Portada

- Muestra cada artículo con su título, su tipo, su fecha en español (día, nombre del mes y año) y un extracto del cuerpo.
- Ofrece cuatro filtros: Todas, Moneda, Billete y Medalla. El filtro solo oculta tarjetas; no borra artículos. «Todas» muestra el gabinete completo.
- Si el filtro elegido no tiene piezas, pero sí hay artículos, se muestra «No hay piezas de este tipo.» No se usa entonces el estado vacío global.
- Si no hay ningún artículo, se muestra el estado vacío y no se muestran los filtros.
- Un artículo sin tipo guardado se etiqueta «Sin clasificar». Entra en «Todas» y no entra en Moneda, Billete ni Medalla.
- El extracto se obtiene así: se recortan los extremos, los saltos y los espacios seguidos pasan a un solo espacio. Si el resultado mide 180 caracteres o menos, se muestra entero. Si mide más, se muestran los primeros 177, se quita el espacio final que haya quedado y se añade el carácter `…`.
- Orden: fecha de publicación descendente. Si hay empate, `createdAt` descendente.
- Cada artículo del listado enlaza con su detalle.
- Si no hay artículos, se muestra el título «El gabinete está vacío», el texto «Todavía no hay piezas catalogadas.» y un enlace «Catalogar la primera pieza» hacia el alta. No se muestra ese estado si hay artículos.
- Cada petición lee la base SQLite. No hay caché de artículos en memoria.

### Detalle

- Muestra título, tipo, fecha de publicación y cuerpo completo. Si no hay tipo guardado, el tipo visible es «Sin clasificar».
- Una línea en blanco separa párrafos. Un salto de línea simple se conserva dentro del párrafo.
- El cuerpo se muestra como texto. Si alguien escribe etiquetas HTML, se ven como texto, no se interpretan.
- Si no hay un artículo con ese identificador, se muestra «Pieza no encontrada», el texto «Ese artículo no está en el gabinete.» y un enlace «Volver al listado». La respuesta HTTP es 404.

### Alta

- Campos obligatorios: título, cuerpo, fecha y tipo.
- El tipo solo puede ser Moneda, Billete o Medalla.
- El título tiene entre 1 y 120 caracteres, sin contar espacios de los extremos.
- El cuerpo tiene entre 1 y 20000 caracteres, sin contar espacios de los extremos.
- La fecha es un día real del calendario en formato `AAAA-MM-DD`. El formulario usa un selector de fecha y propone el día de hoy.
- Si los datos son válidos, se crea el artículo, se guarda en SQLite y el navegador abre su detalle.
- Si no son válidos, no se escribe nada y se muestra el mensaje junto al campo:

| Campo | Situación | Mensaje |
| --- | --- | --- |
| Título | Vacío | El título es obligatorio |
| Título | Más de 120 caracteres | El título admite como máximo 120 caracteres |
| Cuerpo | Vacío | El cuerpo es obligatorio |
| Cuerpo | Más de 20000 caracteres | El cuerpo admite como máximo 20000 caracteres |
| Fecha | Vacía | La fecha es obligatoria |
| Fecha | Formato incorrecto o día imposible | La fecha debe ser un día real con el formato AAAA-MM-DD |
| Tipo | Vacío | El tipo es obligatorio |
| Tipo | Distinto de Moneda, Billete o Medalla | El tipo debe ser Moneda, Billete o Medalla |

- El identificador sale del título: minúsculas, sin acentos, con guiones. Si ya existe, se añade un sufijo numérico. No se pide al autor.

### Datos de ejemplo

La migración inicial carga cuatro artículos, para poder recorrer portada, detalle y filtros sin crear nada:

- «La onza sevillana y el oro del Guadalquivir» (2026-10-29, Moneda)
- «Cuando la peseta se hizo papel» (2026-09-18, Billete)
- «Cómo leer la ceca de una moneda» (2026-06-02, Moneda)
- «El real de a ocho, la moneda que dio la vuelta al mundo» (2026-03-12, Moneda)

En la portada, con el filtro Todas, se ven en este orden: onza, peseta, ceca, real de a ocho.

## 7. Requisitos no funcionales

- Se ejecuta en local con Python 3.12 o 3.13, Django y uv. El entorno virtual es `.venv`.
- La interfaz está en español y la genera el servidor. Portada, detalle, alta y filtros funcionan sin JavaScript.
- Una sola columna, legible en un portátil y en un móvil estrecho.
- El aspecto puede afinarse sin cambiar este PRD mientras sigan viéndose los mismos datos y las mismas acciones.

## 8. Rutas locales

| Ruta | Resultado |
| --- | --- |
| `GET /` | Portada. `?tipo=Moneda`, `Billete` o `Medalla` filtra. |
| `GET /articulo/<identificador>/` | Detalle, o 404 si no existe. |
| `GET /nueva/` | Formulario de alta. |
| `POST /nueva/` | Crea el artículo y abre su detalle, o vuelve a mostrar los errores. |

La interfaz MCP local (`servidor_mcp.py`, `http://127.0.0.1:8001/mcp`) ofrece las mismas tres operaciones: listar, abrir por identificador y publicar. Publicar exige título, cuerpo, fecha y tipo, con los mensajes de esta sección. No hay borradores.

## 9. Criterios de aceptación

La lista verificable, con el mismo texto, está en `spec/acceptance_criteria.md`.

- AC-1. La portada lista título, fecha en español y extracto, de más reciente a más antiguo.
- AC-2. Sin artículos, la portada muestra el estado vacío y el enlace de alta.
- AC-3. El detalle muestra título, fecha y cuerpo, con párrafos separados por línea en blanco.
- AC-4. Un detalle inexistente muestra el aviso y responde 404.
- AC-5. Un alta válida (título, cuerpo, fecha y tipo) crea el artículo, lo guarda y abre su detalle.
- AC-6. Un alta inválida no guarda nada y muestra el mensaje del campo, también si el tipo falta o no está admitido.
- AC-7. El artículo creado aparece en la portada en la posición que le toca por fecha.
- AC-8. El artículo sigue en SQLite después de reiniciar el servidor.
- AC-9. `uv sync`, `migrate` y `runserver` dejan el blog en `http://127.0.0.1:8080`.
- AC-10. El tipo guardado es exactamente Moneda, Billete o Medalla.
- AC-11. La portada filtra por tipo sin borrar, distingue el filtro vacío del gabinete vacío y etiqueta como «Sin clasificar» lo que no tiene tipo.
- AC-12. El detalle muestra el tipo.

## 10. Verificación

- Automática: `uv run python manage.py test` cubre orden, validación, alta, 404, filtros y persistencia.
- Manual en el navegador: portada, extracto, detalle, formulario, errores visibles y estado vacío.

## 11. Cambio de alcance

Cualquier capacidad nueva se escribe antes en este PRD y en `spec/`. Después se implementa y se vuelve a comprobar la lista anterior.
