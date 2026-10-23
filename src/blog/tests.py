from datetime import timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.admin import ArticleAdmin, CategoryAdmin
from blog.models import Article, Category


class HomeAcceptanceTests(TestCase):
    def setUp(self):
        conservation, _created = Category.objects.get_or_create(
            slug="conservacion",
            defaults={"name": "Conservación"},
        )
        identification, _created = Category.objects.get_or_create(
            slug="identificacion",
            defaults={"name": "Identificación"},
        )
        now = timezone.now()
        self.older = Article.objects.create(
            title="Cómo guardar una moneda",
            slug="como-guardar-una-moneda",
            author="Luis Ferrer",
            summary="Un estuche seco evita el deterioro.",
            category=conservation,
            is_published=True,
            published_at=now - timedelta(days=10),
        )
        self.newer = Article.objects.create(
            title="Cómo leer el año de una moneda",
            slug="como-leer-el-ano",
            author="Ana Ríos",
            summary="El año suele estar en el anverso.",
            body="Lee la fecha con buena luz y no fuerces la pieza.",
            category=identification,
            is_published=True,
            published_at=now,
        )
        Article.objects.create(
            title="Borrador interno",
            slug="borrador-interno",
            author="Marta Soler",
            summary="Esto no debe verse.",
            body="Texto oculto del borrador.",
            category=conservation,
            is_published=False,
            published_at=now + timedelta(days=1),
        )

    def test_ca01_home_lists_published_articles_newest_first(self):
        response = self.client.get(reverse("blog:home"))

        self.assertEqual(response.status_code, 200)
        articles = list(response.context["articles"])
        self.assertIn(self.newer, articles)
        self.assertIn(self.older, articles)
        self.assertLess(articles.index(self.newer), articles.index(self.older))
        self.assertTrue(all(article.is_published for article in articles))
        self.assertNotIn(
            "borrador-interno",
            [article.slug for article in articles],
        )

    def test_ca02_listing_shows_title_category_summary_and_detail_link(self):
        response = self.client.get(reverse("blog:home"))

        self.assertContains(response, self.newer.title)
        self.assertContains(response, self.newer.author)
        self.assertContains(response, self.newer.category.name)
        self.assertContains(response, self.newer.summary)
        self.assertContains(
            response,
            reverse("blog:article_detail", args=[self.newer.slug]),
        )
        self.assertNotContains(response, "Borrador interno")

    def test_article_page_shows_title_and_author(self):
        response = self.client.get(
            reverse("blog:article_detail", args=[self.newer.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.newer.title)
        self.assertContains(response, self.newer.author)
        self.assertContains(response, self.newer.body)
        self.assertContains(response, reverse("blog:home"))
        self.assertContains(
            response,
            reverse("blog:category_detail", args=[self.newer.category.slug]),
        )

    def test_category_page_lists_only_its_published_articles(self):
        response = self.client.get(
            reverse("blog:category_detail", args=["identificacion"])
        )

        self.assertEqual(response.status_code, 200)
        articles = list(response.context["articles"])
        self.assertEqual(articles, [self.newer])
        self.assertContains(response, self.newer.author)
        self.assertContains(response, self.newer.summary)
        self.assertNotContains(response, self.older.title)
        self.assertNotContains(response, "Borrador interno")
        self.assertContains(response, reverse("blog:home"))

    def test_unpublished_article_url_does_not_show_content(self):
        response = self.client.get(
            reverse("blog:article_detail", args=["borrador-interno"])
        )

        self.assertEqual(response.status_code, 404)
        self.assertNotContains(response, "Esto no debe verse.", status_code=404)
        self.assertNotContains(response, "Texto oculto del borrador.", status_code=404)

    def test_public_pages_need_no_login_and_state_they_are_not_an_appraisal(self):
        response = self.client.get(reverse("blog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="viewport"')
        self.assertContains(
            response,
            "No son una tasación ni un dictamen profesional",
        )

    def test_stylesheet_adapts_to_small_screens(self):
        css = (
            Path(__file__).resolve().parent / "static" / "blog" / "library.css"
        ).read_text(encoding="utf-8")

        self.assertIn("@media", css)
        self.assertIn("--leather", css)

    def test_initial_topics_and_timestamps(self):
        slugs = set(Category.objects.values_list("slug", flat=True))
        self.assertTrue(
            {"conservacion", "identificacion", "series-habituales"}.issubset(slugs)
        )
        series = Article.objects.get(slug="que-es-una-serie")
        self.assertTrue(series.is_published)
        self.assertLess(len(series.summary.split()), 40)
        self.assertIsNotNone(self.newer.created_at)
        self.assertIsNotNone(self.newer.updated_at)


class AdminAcceptanceTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin = user_model.objects.create_superuser(
            username="editor",
            email="editor@example.com",
            password="clave-segura-123",
        )
        self.client.force_login(self.admin)
        self.category = Category.objects.create(
            name="Conservación de prueba",
            slug="conservacion-de-prueba",
        )

    def test_admin_configuration_matches_the_criteria(self):
        self.assertEqual(CategoryAdmin.prepopulated_fields, {"slug": ("name",)})
        self.assertEqual(ArticleAdmin.prepopulated_fields, {"slug": ("title",)})
        self.assertEqual(ArticleAdmin.search_fields, ("title",))
        self.assertEqual(
            ArticleAdmin.list_display,
            ("title", "category", "publication_status"),
        )
        self.assertEqual(
            ArticleAdmin.publication_status.short_description,
            "estado de publicación",
        )
        self.assertIn("created_at", ArticleAdmin.readonly_fields)
        self.assertIn("updated_at", ArticleAdmin.readonly_fields)

    def test_admin_creates_category_with_unique_slug(self):
        created = self.client.post(
            reverse("admin:blog_category_add"),
            {"name": "Series de prueba", "slug": "series-de-prueba"},
        )
        self.assertEqual(created.status_code, 302)
        self.assertTrue(Category.objects.filter(slug="series-de-prueba").exists())

        duplicate = self.client.post(
            reverse("admin:blog_category_add"),
            {"name": "Otra", "slug": "series-de-prueba"},
        )
        self.assertEqual(duplicate.status_code, 200)
        self.assertEqual(
            Category.objects.filter(slug="series-de-prueba").count(),
            1,
        )

    def test_admin_publishes_and_hides_an_article_without_code_changes(self):
        created = self.client.post(
            reverse("admin:blog_article_add"),
            {
                "title": "Cómo empezar una serie",
                "slug": "como-empezar-una-serie",
                "author": "Clara Nieto",
                "summary": "Elige un diseño y anota los años que ya tienes.",
                "body": "Una guía breve para ordenar las primeras piezas.",
                "category": self.category.pk,
                "published_at_0": "2026-10-01",
                "published_at_1": "10:00:00",
                "is_published": "on",
            },
        )
        self.assertEqual(created.status_code, 302, created.content.decode())
        article = Article.objects.get(slug="como-empezar-una-serie")
        self.assertIsNotNone(article.created_at)
        self.assertIsNotNone(article.updated_at)

        self.client.logout()
        public = self.client.get(reverse("blog:article_detail", args=[article.slug]))
        self.assertContains(public, article.body)

        self.client.force_login(self.admin)
        hidden = self.client.post(
            reverse("admin:blog_article_change", args=[article.pk]),
            {
                "title": article.title,
                "slug": article.slug,
                "author": article.author,
                "summary": article.summary,
                "body": article.body,
                "category": self.category.pk,
                "published_at_0": "2026-10-01",
                "published_at_1": "10:00:00",
            },
        )
        self.assertEqual(hidden.status_code, 302, hidden.content.decode())

        self.client.logout()
        hidden_page = self.client.get(
            reverse("blog:article_detail", args=[article.slug])
        )
        self.assertEqual(hidden_page.status_code, 404)
        home = self.client.get(reverse("blog:home"))
        self.assertNotContains(home, article.title)

    def test_article_changelist_shows_status_and_searches_by_title(self):
        Article.objects.create(
            title="Monedas de cobre",
            slug="monedas-de-cobre",
            author="Ana Ríos",
            summary="El cobre se oscurece con la humedad.",
            category=self.category,
            is_published=True,
            published_at=timezone.now(),
        )
        Article.objects.create(
            title="Álbumes para principiantes",
            slug="albumes-para-principiantes",
            author="Luis Ferrer",
            summary="Un álbum pequeño basta al empezar.",
            category=self.category,
            is_published=False,
        )

        changelist = self.client.get(reverse("admin:blog_article_changelist"))
        self.assertContains(changelist, "Monedas de cobre")
        self.assertContains(changelist, self.category.name)
        self.assertContains(changelist, "Estado de publicación")

        search = self.client.get(
            reverse("admin:blog_article_changelist"),
            {"q": "cobre"},
        )
        self.assertContains(search, "Monedas de cobre")
        self.assertNotContains(search, "Álbumes para principiantes")
