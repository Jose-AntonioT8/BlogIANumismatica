from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'piece_type', 'published_on', 'slug')
    list_filter = ('piece_type',)
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
