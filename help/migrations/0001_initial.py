# Generated by Django 3.2.4 on 2022-10-06 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HelpPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('url_tag', models.CharField(max_length=20, unique=True, verbose_name='URL тег адреса')),
            ],
            options={
                'verbose_name': 'Помощь',
                'verbose_name_plural': 'Помощь',
            },
        ),
    ]
