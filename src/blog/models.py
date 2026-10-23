from django.db import models
from django.db.models import F


class Category(models.Model):
    name = models.CharField("nombre", max_length=100)
    slug = models.SlugField("slug", max_length=100, unique=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PublishedArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True).order_by(
            F("published_at").desc(nulls_last=True)
        )


class Article(models.Model):
    title = models.CharField("título", max_length=200)
    slug = models.SlugField("slug", max_length=200, unique=True)
    author = models.CharField("autor", max_length=120)
    summary = models.TextField("resumen")
    body = models.TextField("cuerpo", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles",
        verbose_name="categoría",
    )
    published_at = models.DateTimeField("fecha de publicación", null=True, blank=True)
    is_published = models.BooleanField("publicado", default=False)
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("fecha de modificación", auto_now=True)

    objects = PublishedArticleQuerySet.as_manager()

    class Meta:
        verbose_name = "artículo"
        verbose_name_plural = "artículos"

    def __str__(self):
        return self.title
