# Generated by Django 4.2.3 on 2023-07-13 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News_Portal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='ratingcomment',
            new_name='rating',
        ),
    ]