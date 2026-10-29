from .forms import ArticleForm
from .models import Article, unique_slug
from .text import TIPOS, excerpt, fecha_es

_CAMPOS = {
    'title': 'titulo',
    'body': 'cuerpo',
    'published_on': 'fecha',
    'piece_type': 'tipo',
}


def a_dict(article):
    return {
        'identificador': article.slug,
        'titulo': article.title,
        'cuerpo': article.body,
        'fecha': article.published_on.isoformat(),
        'fecha_texto': fecha_es(article.published_on),
        'tipo': article.piece_type,
        'etiqueta': article.label,
        'extracto': excerpt(article.body),
        'creado': article.created_at.isoformat(),
        'ruta': f'/articulo/{article.slug}/',
    }


def listar(tipo=''):
    chosen = (tipo or '').strip()
    articles = Article.objects.all()
    if chosen and chosen != 'Todas':
        if chosen not in TIPOS:
            raise ValueError('El tipo debe ser Moneda, Billete o Medalla')
        articles = articles.filter(piece_type=chosen)
    return [a_dict(article) for article in articles]


def obtener(identificador):
    article = Article.objects.filter(slug=(identificador or '').strip()).first()
    if article is None:
        raise ValueError('Artículo no encontrado')
    return a_dict(article)


def crear(titulo, cuerpo, fecha, tipo):
    form = ArticleForm(data={
        'title': titulo,
        'body': cuerpo,
        'published_on': fecha,
        'piece_type': tipo,
    })
    if not form.is_valid():
        campos = {}
        for name, errors in form.errors.items():
            campos[_CAMPOS.get(name, name)] = errors[0]
        return {
            'ok': False,
            'error': 'Revisa los campos señalados',
            'campos': campos,
        }
    article = form.save(commit=False)
    article.slug = unique_slug(article.title)
    article.save()
    return {'ok': True, 'articulo': a_dict(article)}
