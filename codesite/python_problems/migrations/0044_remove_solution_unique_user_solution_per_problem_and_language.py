from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("python_problems", "0043_alter_problem_difficulty_alter_problem_method_name_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="solution",
            name="unique_user_solution_per_problem_and_language",
        ),
    ]
