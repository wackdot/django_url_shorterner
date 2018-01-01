# Generated by Django 2.0 on 2017-12-31 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SavedEmbeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=15)),
                ('provider_url', models.URLField()),
                ('provider_name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('html', models.TextField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('thumbnail_url', models.URLField()),
                ('thumbnail_width', models.IntegerField()),
                ('thumbnail_height', models.IntegerField()),
                ('author_url', models.URLField()),
                ('author_name', models.CharField(max_length=100)),
                ('version', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]
