# Generated by Django 5.0.6 on 2024-06-15 19:06

from django.db import migrations, models
import django.utils.timezone
from datetime import timedelta
import random
import pytz


def set_sequential_dates(apps, _):
    Problem = apps.get_model('python_problems', 'Problem')

    start_date = django.utils.timezone.datetime(2024, 2, 1, tzinfo=pytz.UTC)
    end_date = django.utils.timezone.now()
    total_days = (end_date - start_date).days
    # Prevent division by zero
    increment = total_days / max(1, Problem.objects.count() - 1)

    current_date = start_date

    for problem in Problem.objects.all().order_by('id'):
        created_at = current_date
        problem.created_at = created_at
        problem.updated_at = created_at
        problem.save()
        current_date += timedelta(days=increment)


class Migration(migrations.Migration):

    dependencies = [
        ('python_problems', '0017_remove_problem_is_solved'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.RunPython(set_sequential_dates),
        migrations.AlterField(
            model_name='problem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
