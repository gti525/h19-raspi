# Generated by Django 2.1.7 on 2019-03-07 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0014_auto_20190307_2120'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Seller',
        ),
        migrations.RemoveField(
            model_name='show',
            name='venue',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='show',
        ),
        migrations.DeleteModel(
            name='Show',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.DeleteModel(
            name='Venue',
        ),
    ]
