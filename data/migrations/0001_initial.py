# Generated by Django 2.2.5 on 2020-10-19 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('link', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('caption', models.TextField()),
                ('tahun', models.CharField(max_length=225)),
                ('label', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'data_instagram',
            },
        ),
    ]