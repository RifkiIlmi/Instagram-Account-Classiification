# Generated by Django 2.2.5 on 2020-10-21 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klasifikasi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klasifikasi',
            name='tf_idf_dict',
            field=models.CharField(max_length=225),
        ),
    ]
