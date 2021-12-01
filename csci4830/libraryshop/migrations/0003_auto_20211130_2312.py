# Generated by Django 3.2.9 on 2021-11-30 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryshop', '0002_auto_20211115_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='booksection',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
