# Generated by Django 2.1.7 on 2019-03-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0003_auto_20190319_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='artist',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
