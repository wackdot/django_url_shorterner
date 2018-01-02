# Generated by Django 2.0 on 2018-01-02 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10)),
                ('created', models.DateTimeField()),
                ('short_url_clicks', models.IntegerField()),
                ('long_url_clicks', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Browsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Platforms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Referrers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TwoHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('user_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('short_url', models.CharField(max_length=200)),
                ('input_url', models.CharField(max_length=200)),
                ('analytics', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='shorterner.Analytics')),
            ],
        ),
        migrations.AddField(
            model_name='week',
            name='analytics_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shorterner.Analytics'),
        ),
        migrations.AddField(
            model_name='twohours',
            name='analytics_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shorterner.Analytics'),
        ),
        migrations.AddField(
            model_name='referrers',
            name='analytics_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shorterner.Analytics'),
        ),
        migrations.AddField(
            model_name='platforms',
            name='analytics_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shorterner.Analytics'),
        ),
        migrations.AddField(
            model_name='month',
            name='analytics_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shorterner.Analytics'),
        ),
        migrations.AddField(
            model_name='day',
            name='analytics_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shorterner.Analytics'),
        ),
        migrations.AddField(
            model_name='countries',
            name='analytics_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shorterner.Analytics'),
        ),
        migrations.AddField(
            model_name='browsers',
            name='analytics_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shorterner.Analytics'),
        ),
    ]
