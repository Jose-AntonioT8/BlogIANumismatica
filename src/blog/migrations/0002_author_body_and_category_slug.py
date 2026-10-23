from django.db import migrations, models
from django.utils.text import slugify


def fill_category_slugs(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    used = set()
    for category in Category.objects.all():
        base = slugify(category.name) or "categoria"
        slug = base
        suffix = 2
        while slug in used:
            slug = f"{base}-{suffix}"
            suffix += 1
        category.slug = slug
        category.save(update_fields=["slug"])
        used.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=100, null=True, verbose_name="slug"),
        ),
        migrations.RunPython(fill_category_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=100, unique=True, verbose_name="slug"),
        ),
        migrations.AddField(
            model_name="article",
            name="author",
            field=models.CharField(default="", max_length=120, verbose_name="autor"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="article",
            name="body",
            field=models.TextField(blank=True, default="", verbose_name="cuerpo"),
            preserve_default=False,
        ),
    ]
