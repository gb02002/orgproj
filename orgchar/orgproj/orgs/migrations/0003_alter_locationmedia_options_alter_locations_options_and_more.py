# Generated by Django 5.0.2 on 2024-03-25 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0002_locationmedia_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locationmedia',
            options={'verbose_name': 'Медиа-файл', 'verbose_name_plural': 'Медиа-файлы'},
        ),
        migrations.AlterModelOptions(
            name='locations',
            options={'verbose_name': 'Локация', 'verbose_name_plural': 'Локации'},
        ),
        migrations.AlterModelOptions(
            name='organisation',
            options={'verbose_name': 'Организации', 'verbose_name_plural': 'Организации'},
        ),
    ]