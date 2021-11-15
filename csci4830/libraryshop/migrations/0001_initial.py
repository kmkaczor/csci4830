# Generated by Django 3.2.9 on 2021-11-15 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import libraryshop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=60, null=True)),
                ('lastname', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_edit_db', models.DateField(auto_created=True, auto_now=True)),
                ('date_added_db', models.DateField(auto_created=True, auto_now_add=True)),
                ('title', models.CharField(max_length=250)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('ISBN', models.CharField(blank=True, max_length=14, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('cover_image', models.ImageField(blank=True, max_length=250, null=True, upload_to=libraryshop.models.Book.cover_image_path)),
                ('genre', models.CharField(blank=True, choices=[('HORROR', 'Horror'), ('ROMANC', 'Romance'), ('NONFIC', 'Non-fiction'), ('FANTAS', 'Fantasy'), ('SCIFIC', 'Science Fiction'), ('MYSTER', 'Mystery'), ('HSTFIC', 'Historial Fiction'), ('CHLDRN', 'Childrens'), ('ATOBIO', 'Autobiography'), ('PHILOS', 'Philosophy'), ('HISTRY', 'History'), ('COOKBK', 'Cookbook')], max_length=6)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryshop.author')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserOwnBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='libraryshop.book')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_title', models.CharField(max_length=1000, null=True)),
                ('chapter_num', models.PositiveIntegerField(verbose_name='Chapter number')),
                ('file', models.FileField(max_length=250, unique=True, upload_to=libraryshop.models.BookSection.book_section_path)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='libraryshop.book')),
            ],
        ),
        migrations.CreateModel(
            name='BookCollectionMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='libraryshop.book')),
                ('collection_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='libraryshop.collection')),
            ],
        ),
        migrations.AddConstraint(
            model_name='userownbook',
            constraint=models.UniqueConstraint(fields=('user_id', 'book_id'), name='constraint_book_owner'),
        ),
        migrations.AddConstraint(
            model_name='booksection',
            constraint=models.UniqueConstraint(fields=('book_id', 'chapter_num'), name='constraint_book_chapter'),
        ),
    ]
