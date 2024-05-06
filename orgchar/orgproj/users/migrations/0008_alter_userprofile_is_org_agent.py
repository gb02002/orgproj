# Generated by Django 5.0.2 on 2024-05-06 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_userprofile_confirmed_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_org_agent',
            field=models.CharField(choices=[('None', 'None'), ('pending', 'Pending'), ('confirmed', 'Confirmed')], default='None', max_length=20, verbose_name='confirmed user'),
        ),
    ]