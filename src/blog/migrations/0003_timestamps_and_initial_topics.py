import django.utils.timezone
from django.db import migrations, models


def seed_initial_topics(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    Article = apps.get_model("blog", "Article")
    now = django.utils.timezone.now()
    topics = [
        ("Conservación", "conservacion"),
        ("Identificación", "identificacion"),
        ("Series habituales", "series-habituales"),
    ]
    categories = {}
    for name, slug in topics:
        category, _created = Category.objects.get_or_create(
            slug=slug,
            defaults={"name": name},
        )
        if category.name != name:
            category.name = name
            category.save(update_fields=["name"])
        categories[slug] = category

    Article.objects.get_or_create(
        slug="que-es-una-serie",
        defaults={
            "title": "Qué es una serie",
            "author": "Clara Nieto",
            "summary": "Una serie reúne piezas con un mismo diseño a lo largo de varios años.",
            "body": (
                "Para empezar, observa el diseño que se repite y anota el año. "
                "Esta nota solo orienta: la autenticidad y el valor los determina un profesional."
            ),
            "category": categories["series-habituales"],
            "is_published": True,
            "published_at": now,
            "created_at": now,
            "updated_at": now,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_author_body_and_category_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="fecha de creación",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="article",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                default=django.utils.timezone.now,
                verbose_name="fecha de modificación",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(seed_initial_topics, migrations.RunPython.noop),
    ]
