# Generated by Django 2.1.7 on 2019-04-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0006_auto_20190329_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='remote_id',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='showpublication',
            name='remote_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
