from django.db import migrations
from django.utils.dateparse import parse_date, parse_datetime


def load_examples(apps, schema_editor):
    Article = apps.get_model('articulos', 'Article')
    from articulos.seed_data import EXAMPLES

    for item in EXAMPLES:
        Article.objects.update_or_create(
            slug=item['slug'],
            defaults={
                'title': item['title'],
                'body': item['body'],
                'published_on': parse_date(item['published_on']),
                'piece_type': item['piece_type'],
                'created_at': parse_datetime(item['created_at']),
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ('articulos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_examples, migrations.RunPython.noop),
    ]
