# Generated by Django 4.2.7 on 2024-06-19 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('python_problems', '0027_solution_unique_solution_per_problem_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='solution',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='testcase',
        ),
    ]
