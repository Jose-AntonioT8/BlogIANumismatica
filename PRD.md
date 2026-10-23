# PRD: blog sobre numismática con Django

## 1. Resumen

Crear un blog en Django para que las personas que empiezan en la numismática puedan encontrar y leer consejos básicos sobre la identificación, la conservación y el coleccionismo de monedas. El contenido se gestionará desde el panel de administración de Django y será de solo lectura para los visitantes.

## 2. Objetivo

Permitir que un visitante encuentre y lea fácilmente artículos breves y comprensibles sobre numismática, sin necesidad de registrarse.

## 3. Usuarios

- **Visitante:** consulta artículos y los explora por categoría.
- **Editor o administrador:** crea, modifica, publica y organiza artículos desde Django Admin.

## 4. Alcance de la primera versión

### Incluye

- Página de inicio con los artículos publicados, ordenados del más reciente al más antiguo.
- Listado de artículos de una categoría.
- Página de detalle para cada artículo.
- Gestión de categorías y artículos desde Django Admin.
- Diseño adaptable a móviles y ordenadores.

### No incluye

- Registro de visitantes, comentarios o valoraciones.
- Tienda en línea.
- Buscador, etiquetas o recomendaciones personalizadas.
- Editor de texto enriquecido ni flujo de aprobación con varios roles.

## 5. Requisitos de Django

### Aplicación y datos

Crear una aplicación Django para el blog con estos modelos:

- **Category**
  - `name`: nombre visible de la categoría.
  - `slug`: identificador para la URL, único.

- **Article**
  - `title`: título del artículo.
  - `slug`: identificador para la URL, único.
  - `author`: nombre del autor, visible en los listados y dentro del artículo.
  - `summary`: resumen breve para los listados.
  - `body`: contenido del artículo.
  - `category`: relación obligatoria con `Category`.
  - `created_at`: fecha de creación automática.
  - `updated_at`: fecha de modificación automática.
  - `published_at`: fecha y hora de publicación, opcional hasta publicar.
  - `is_published`: indica si el artículo es visible públicamente.

Usar las migraciones de Django para crear y modificar el esquema de la base de datos. La configuración inicial puede utilizar SQLite.

### Administración de contenido

- Registrar `Category` y `Article` en Django Admin.
- Permitir editar todos los campos necesarios y buscar artículos por título.
- Mostrar título, categoría y estado de publicación en la lista de artículos.
- Los artículos en borrador no deben aparecer en las páginas públicas.

### Vistas y URLs

- `GET /`: página de inicio con los artículos publicados.
- `GET /categoria/<slug>/`: artículos publicados de una categoría.
- `GET /articulo/<slug>/`: detalle de un artículo publicado.

Las vistas públicas pueden implementarse con vistas genéricas de Django (`ListView` y `DetailView`) o vistas equivalentes. Las consultas deben limitar los resultados a artículos publicados y ordenarlos por fecha de publicación descendente.

### Plantillas y estáticos

- Crear plantillas para la página de inicio, el listado por categoría y el detalle del artículo.
- Reutilizar una plantilla base para navegación y estructura común.
- Usar archivos estáticos de Django para los estilos CSS.
- Mostrar enlaces a categorías y permitir volver al inicio desde las páginas interiores.

## 6. Requisitos de contenido y diseño

- Los artículos deben ser breves, claros y adecuados para principiantes.
- Los temas iniciales serán conservación de las monedas, identificación de piezas y series habituales para quien empieza.
- La interfaz será amigable, con estilo de biblioteca y colores amarronados, y facilitará la lectura en pantallas pequeñas y grandes.
- El inicio muestra el autor de cada artículo. La página del artículo muestra el título y el autor.
- El contenido será divulgativo y no sustituirá la tasación ni el dictamen de un profesional sobre autenticidad o valor.

## 7. Criterios de aceptación

- Un visitante puede abrir la página de inicio y ver los artículos publicados ordenados por fecha.
- Cada artículo del listado muestra título, autor, categoría y resumen, y enlaza a su página de detalle.
- La página de una categoría solo muestra artículos publicados asociados a ella.
- La URL de un artículo publicado muestra el título, el autor y su contenido completo.
- Un artículo no publicado no aparece en listados ni se puede consultar desde su URL pública.
- Un administrador puede crear y modificar categorías y artículos desde Django Admin.
- Las páginas públicas se pueden usar en móvil y ordenador y no requieren iniciar sesión.

## 8. Indicador de éxito

Una persona sin cuenta puede encontrar un artículo por su categoría y leerlo; un administrador puede mantener el contenido desde Django Admin sin modificar código.
