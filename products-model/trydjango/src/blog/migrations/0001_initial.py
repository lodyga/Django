# Generated by Django 5.0.1 on 2024-02-11 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titile', models.CharField(max_length=120)),
                ('concent', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]