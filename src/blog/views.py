from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from blog.models import Article, Category


class ArticleListView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "blog/home.html"

    def get_queryset(self):
        return Article.objects.published().select_related("category")


class CategoryArticleListView(ListView):
    context_object_name = "articles"
    template_name = "blog/category_list.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])

    def get_queryset(self):
        return (
            Article.objects.published()
            .filter(category=self.category)
            .select_related("category")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = "article"
    template_name = "blog/article_detail.html"

    def get_queryset(self):
        return Article.objects.published().select_related("category")
