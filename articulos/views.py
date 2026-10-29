from datetime import date

from django.shortcuts import redirect, render

from .forms import ArticleForm
from .models import Article, unique_slug
from .text import TIPOS


def index(request):
    selected = request.GET.get('tipo', 'Todas')
    if selected not in ('Todas', *TIPOS):
        selected = 'Todas'
    articles = Article.objects.all()
    total = articles.count()
    if selected != 'Todas':
        articles = articles.filter(piece_type=selected)
    return render(request, 'articulos/index.html', {
        'articles': articles,
        'total': total,
        'selected': selected,
        'filters': ('Todas', *TIPOS),
        'section': 'portada',
    })


def detail(request, slug):
    article = Article.objects.filter(slug=slug).first()
    if article is None:
        return render(request, 'articulos/missing.html', status=404)
    return render(request, 'articulos/detail.html', {
        'article': article,
        'section': 'detalle',
    })


def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.slug = unique_slug(article.title)
            article.save()
            return redirect('detail', slug=article.slug)
    else:
        form = ArticleForm(initial={'published_on': date.today().isoformat()})
    return render(request, 'articulos/create.html', {
        'form': form,
        'section': 'nueva',
    })
