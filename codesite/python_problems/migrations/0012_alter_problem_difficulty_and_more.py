# Generated by Django 4.2.7 on 2024-05-13 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('python_problems', '0011_problem_space_complexity_problem_time_complexity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='problems_difficulty', to='python_problems.difficulty'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='space_complexity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='problems_space_complexity', to='python_problems.complexity'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='time_complexity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='problems_time_complexity', to='python_problems.complexity'),
        ),
    ]
