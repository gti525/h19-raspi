# Generated by Django 2.1.7 on 2019-04-04 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0007_auto_20190401_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='sellers',
            field=models.ManyToManyField(to='venue.Seller'),
        ),
    ]
