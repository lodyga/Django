# Generated by Django 5.0.6 on 2024-06-15 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('python_problems', '0016_alter_problem_title_alter_tag_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='is_solved',
        ),
    ]
