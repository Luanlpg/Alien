# Generated by Django 2.2 on 2019-04-21 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroglifos', '0004_auto_20190420_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agroglifos',
            name='url',
            field=models.URLField(default='-- -- --', max_length=300),
        ),
    ]
