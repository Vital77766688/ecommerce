# Generated by Django 3.1.6 on 2021-03-05 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_useraddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='building_number',
            field=models.CharField(max_length=10, verbose_name='# of building'),
        ),
    ]
