# Generated by Django 4.2.7 on 2025-04-01 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('python_problems', '0038_alter_solution_language_alter_solution_problem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solution',
            old_name='test_case',
            new_name='test_cases',
        ),
    ]
