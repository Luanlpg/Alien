# Generated by Django 2.2 on 2019-04-20 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroglifos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agroglifos',
            name='description',
            field=models.CharField(default='N/D', max_length=900),
        ),
    ]