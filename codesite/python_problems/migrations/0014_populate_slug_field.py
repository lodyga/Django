# Generated by Django 4.2.7 on 2024-05-26 16:14

from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Problem = apps.get_model('python_problems', 'Problem')
    for problem in Problem.objects.all():
        if not problem.slug:
            problem.slug = slugify(problem.title)
            problem.save()


class Migration(migrations.Migration):

    dependencies = [
        ('python_problems', '0013_add_slug_field'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
        migrations.AlterField(
            model_name='problem',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]