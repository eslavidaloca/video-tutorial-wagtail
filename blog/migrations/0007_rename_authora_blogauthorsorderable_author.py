# Generated by Django 4.1.7 on 2023-03-22 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_author_blogauthorsorderable_authora'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogauthorsorderable',
            old_name='authora',
            new_name='author',
        ),
    ]