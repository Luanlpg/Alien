# Generated by Django 2.2 on 2019-04-20 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroglifos', '0003_agroglifos_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agroglifos',
            name='date',
            field=models.DateField(),
        ),
    ]