# Generated by Django 2.0 on 2018-01-03 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ErrorDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=200)),
                ('required', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=200)),
                ('locationType', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url_clicks', models.IntegerField()),
                ('long_url_clicks', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PeriodDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('source_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.CharField(max_length=200)),
                ('input_url', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=10)),
                ('created', models.DateTimeField()),
                ('alltime', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='urls_alltime', related_query_name='shorterner_urlss', to='shorterner.Period')),
                ('day', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='urls_day', related_query_name='shorterner_urlss', to='shorterner.Period')),
                ('month', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='urls_month', related_query_name='shorterner_urlss', to='shorterner.Period')),
                ('twohours', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='urls_twohours', related_query_name='shorterner_urlss', to='shorterner.Period')),
                ('week', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='urls_week', related_query_name='shorterner_urlss', to='shorterner.Period')),
            ],
        ),
        migrations.AddField(
            model_name='period',
            name='browsers',
            field=models.ManyToManyField(blank=True, related_name='period_browsers', related_query_name='shorterner_periods', to='shorterner.PeriodDetails'),
        ),
        migrations.AddField(
            model_name='period',
            name='countries',
            field=models.ManyToManyField(blank=True, related_name='period_countries', related_query_name='shorterner_periods', to='shorterner.PeriodDetails'),
        ),
        migrations.AddField(
            model_name='period',
            name='platforms',
            field=models.ManyToManyField(blank=True, related_name='period_platforms', related_query_name='shorterner_periods', to='shorterner.PeriodDetails'),
        ),
        migrations.AddField(
            model_name='period',
            name='referrers',
            field=models.ManyToManyField(blank=True, related_name='period_referrers', related_query_name='shorterner_periods', to='shorterner.PeriodDetails'),
        ),
        migrations.AddField(
            model_name='error',
            name='error',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shorterner.ErrorDetails'),
        ),
    ]
