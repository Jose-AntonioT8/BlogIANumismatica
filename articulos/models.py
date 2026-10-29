from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from .text import type_label


class Article(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=120)
    body = models.TextField()
    published_on = models.DateField()
    piece_type = models.CharField(max_length=16, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_on', '-created_at']

    def __str__(self):
        return self.title

    @property
    def label(self):
        return type_label(self.piece_type)


def unique_slug(title):
    base = (slugify(title) or 'pieza')[:48].strip('-') or 'pieza'
    candidate = base
    number = 2
    while Article.objects.filter(slug=candidate).exists():
        candidate = f'{base}-{number}'
        number += 1
    return candidate
