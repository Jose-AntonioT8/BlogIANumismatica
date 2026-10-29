# Briefing — El Gabinete

Estado: borrador redactado con asistencia de IA, listo para revisión humana.
Si la revisión cambia una decisión, se actualiza primero el PRD y `spec/`, y después el código.

## Qué queremos

Un blog mínimo de numismática, ejecutable en local, para publicar y leer notas breves sobre monedas, billetes y medallas. El ejercicio sigue un desarrollo guiado por especificación: el alcance se acuerda por escrito antes de implementar.

## Para quién

- Lector: abre la portada, recorre los artículos y entra en uno para leerlo entero.
- Autor: la persona que ejecuta la aplicación en su máquina. Da de alta una pieza con título, cuerpo y fecha.

No hay cuentas ni roles. Quien puede abrir el servidor local puede leer y publicar. Es una limitación aceptada del MVP.

## Por qué este alcance

El enunciado pide tres capacidades: portada con listado, detalle de un artículo y alta con título, cuerpo y fecha. Pide además que funcione en local. Deja fuera la autenticación compleja, los roles, la moderación, el despliegue, el dominio real, los comentarios, el SEO avanzado y el multidioma.

## Decisiones cerradas

| Decisión | Cierre |
| --- | --- |
| Nombre | El Gabinete |
| Idioma de la interfaz y de los textos de ejemplo | Español |
| Ejecución | En el propio equipo, con Python, Django y uv (entorno `.venv`) |
| Datos | SQLite local, a través de los modelos de Django |
| Autoría | Sin login; publica quien usa el servidor local |
| Campos del alta | Título, cuerpo, fecha de publicación y tipo (Moneda, Billete o Medalla). El tipo se añadió en el MVP 1.1; ver `spec/changelog.md`. |
| Orden del listado | Fecha de publicación, de la más reciente a la más antigua |
| Imágenes, comentarios y búsqueda | Fuera de este MVP |

## Cómo sabremos que está listo

Dos personas pueden leer el PRD y describir la misma aplicación. En local se puede abrir la portada, leer un artículo y crear otro que sigue ahí después de reiniciar el servidor. La lista de `spec/acceptance_criteria.md` queda cumplida.

## Revisión humana

Conviene confirmar el nombre, el tono de los artículos de ejemplo y si la fecha de publicación debe elegirla el autor (así está cerrado) o bastaría con la fecha del sistema. El resto del alcance sale del enunciado.
