# Generated by Django 3.0.8 on 2021-01-04 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klasifikasi', '0004_klasifikasiwbigram'),
    ]

    operations = [
        migrations.CreateModel(
            name='HasilAkhir',
            fields=[
                ('link', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('caption', models.TextField()),
                ('username', models.CharField(max_length=225)),
                ('labelold', models.CharField(max_length=100)),
                ('labelnew', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'hasil_akhir',
            },
        ),
    ]
