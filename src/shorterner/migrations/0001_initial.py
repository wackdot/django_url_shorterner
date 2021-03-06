# Generated by Django 2.0 on 2018-01-09 01:48

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
                ('domain', models.CharField(max_length=200)),
                ('reason', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=200)),
                ('locationType', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('code', models.IntegerField()),
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
            name='PeriodDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('source_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.CharField(blank=True, max_length=200)),
                ('input_url', models.CharField(max_length=200)),
                ('status', models.CharField(blank=True, max_length=10)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('alltime', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alltimes', related_query_name='alltime', to='shorterner.Period')),
                ('day', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='days', related_query_name='day', to='shorterner.Period')),
                ('errormessage', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='errormessages', related_query_name='errormessage', to='shorterner.Error')),
                ('month', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='months', related_query_name='month', to='shorterner.Period')),
                ('twohour', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='twohours', related_query_name='twohour', to='shorterner.Period')),
                ('week', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weeks', related_query_name='week', to='shorterner.Period')),
            ],
        ),
        migrations.AddField(
            model_name='period',
            name='browser',
            field=models.ManyToManyField(related_name='browsers', related_query_name='browser', to='shorterner.PeriodDetail'),
        ),
        migrations.AddField(
            model_name='period',
            name='country',
            field=models.ManyToManyField(related_name='countries', related_query_name='country', to='shorterner.PeriodDetail'),
        ),
        migrations.AddField(
            model_name='period',
            name='platform',
            field=models.ManyToManyField(related_name='platforms', related_query_name='platform', to='shorterner.PeriodDetail'),
        ),
        migrations.AddField(
            model_name='period',
            name='referrer',
            field=models.ManyToManyField(related_name='referrers', related_query_name='referrer', to='shorterner.PeriodDetail'),
        ),
    ]
