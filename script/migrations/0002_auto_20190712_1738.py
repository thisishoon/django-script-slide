# Generated by Django 2.2.3 on 2019-07-12 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speechscript',
            name='content',
            field=models.TextField(blank=True, verbose_name='내용'),
        ),
    ]
