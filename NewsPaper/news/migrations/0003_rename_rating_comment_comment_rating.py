# Generated by Django 4.2.2 on 2023-06-25 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_author_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='rating_comment',
            new_name='rating',
        ),
    ]
