# Generated by Django 2.2.5 on 2020-10-19 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='tahun',
            new_name='username',
        ),
    ]
