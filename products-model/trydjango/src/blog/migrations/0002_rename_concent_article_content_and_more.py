# Generated by Django 5.0.1 on 2024-02-12 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='concent',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='titile',
            new_name='title',
        ),
    ]
