# Generated by Django 4.1.7 on 2023-03-22 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogdetailpage_authors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogdetailpage',
            name='authors',
        ),
    ]