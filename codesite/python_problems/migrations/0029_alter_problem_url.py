# Generated by Django 4.2.7 on 2024-06-19 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_problems', '0028_remove_problem_solution_remove_problem_testcase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='url',
            field=models.URLField(),
        ),
    ]
