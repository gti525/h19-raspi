# Generated by Django 2.1.7 on 2019-03-08 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='scanned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]