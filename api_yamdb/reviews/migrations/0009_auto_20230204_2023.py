# Generated by Django 3.2 on 2023-02-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_genretitle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'default_related_name': 'reviews', 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique review'),
        ),
    ]
