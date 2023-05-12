# Generated by Django 4.1.7 on 2023-05-11 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=45, verbose_name='글제목')),
                ('article_content', models.TextField(verbose_name='글내용')),
                ('article_img', models.FileField(blank=True, null=True, upload_to='', verbose_name='이미지')),
                ('article_created_at', models.DateTimeField(auto_now_add=True)),
                ('article_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.CharField(choices=[('cat', '고양이'), ('dog', '개'), ('bird', '새'), ('fish', '물고기'), ('snail', '달팽이'), ('stone', '돌'), ('turtle', '거북이')], max_length=10, verbose_name='반려동물 종류')),
                ('bookmarks', models.ManyToManyField(blank=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
                ('hearts', models.ManyToManyField(blank=True, related_name='hearts', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Article',
                'ordering': ['-article_created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='댓글')),
                ('comment_created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='articles.articles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment',
                'ordering': ['-comment_created_at'],
            },
        ),
    ]