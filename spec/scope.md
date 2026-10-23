# Alcance: blog sobre numismática

Primera versión de un blog en Django. El visitante solo lee. Un editor crea, organiza y publica el contenido desde Django Admin, sin modificar código.

## Incluye

### Páginas públicas

- Página de inicio con los artículos publicados, ordenados del más reciente al más antiguo.
- Listado de los artículos publicados de una categoría en `/categoria/<slug>/`.
- Detalle de cada artículo publicado en `/articulo/<slug>/`. El slug es único y legible, y es el identificador de la URL.
- En cada listado, título, autor, categoría y resumen, con enlace a la página del artículo.
- En la página del artículo, el título y el autor.
- Enlaces a las categorías y regreso al inicio desde las páginas interiores.
- Los borradores no aparecen en los listados ni responden en su URL pública.
- Uso sin registro ni inicio de sesión.

### Contenido

- Categorías con nombre visible y slug único.
- Artículos con título, slug único, autor, resumen, cuerpo, categoría obligatoria, fecha de creación, fecha de modificación, fecha de publicación y estado de publicación.
- Temas iniciales: conservación de las monedas, identificación de piezas y series habituales para quien empieza.
- Textos breves, en lenguaje sencillo y adecuados para principiantes.
- Contenido divulgativo, que no sustituye la tasación ni el dictamen de un profesional sobre autenticidad o valor.

### Administración

- `Category` y `Article` registrados en Django Admin.
- Alta y modificación de categorías y artículos, con todos los campos necesarios.
- Búsqueda de artículos por título.
- Listado de artículos con título, categoría y estado de publicación.

### Presentación y datos

- Plantilla base común y plantillas de inicio, listado por categoría y detalle.
- Estilos CSS servidos como archivos estáticos de Django.
- Diseño limpio y amigable, con estilo de biblioteca y colores amarronados, adaptable a móvil y ordenador.
- Aplicación Django del blog, migraciones y SQLite como base de datos inicial.

## Fuera de esta versión

- Registro de visitantes, comentarios y valoraciones.
- Tienda en línea.
- Buscador, etiquetas y recomendaciones personalizadas.
- Editor de texto enriquecido y flujo de aprobación con varios roles.
