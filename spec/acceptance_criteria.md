# Criterios de aceptación: blog sobre numismática

La primera versión se acepta cuando una persona sin cuenta encuentra un artículo publicado por su categoría y lo lee, y un administrador mantiene el contenido desde Django Admin sin modificar código.

## Lectura pública

- Al abrir `/`, el visitante ve solo artículos publicados, ordenados por fecha de publicación de más reciente a más antigua.
- Cada artículo del listado muestra título, autor, categoría y resumen, y enlaza a su página de detalle.
- `/categoria/<slug>/` muestra solo los artículos publicados de esa categoría, con el mismo orden y los mismos datos del listado.
- `/articulo/<slug>/` de un artículo publicado muestra el título, el autor y su contenido completo. El slug es único, legible y es el identificador de la URL.
- Las páginas interiores enlazan a las categorías y permiten volver al inicio.
- Las páginas públicas se usan en móvil y en ordenador, sin registro ni inicio de sesión.
- El diseño es limpio, legible y tiene una interfaz amigable de biblioteca, con colores amarronados.

## Borradores

- Un artículo no publicado no aparece en el inicio ni en el listado de su categoría.
- La URL pública de un artículo no publicado no muestra su contenido.

## Administración

- Desde Django Admin se crean y modifican categorías, con nombre visible y slug único.
- Desde Django Admin se crean y modifican artículos, con título, slug único, autor, resumen, cuerpo, categoría obligatoria, fecha de publicación y estado de publicación.
- La fecha de creación y la de modificación se registran solas.
- La lista de artículos muestra título, categoría y estado de publicación, y permite buscar por título.
- Publicar u ocultar un artículo desde Django Admin cambia lo que ve el visitante, sin modificar código.

## Contenido

- Los artículos publicados son breves, claros y adecuados para quien empieza en la numismática.
- El contenido puede organizarse en los temas iniciales: conservación de las monedas, identificación de piezas y series habituales para quien empieza.
- El contenido es divulgativo y no se presenta como tasación ni como dictamen profesional sobre autenticidad o valor.
