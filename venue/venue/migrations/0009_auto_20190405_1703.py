# Generated by Django 2.1.7 on 2019-04-05 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venue', '0008_show_sellers'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketValidator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='validators', to='venue.Show')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='validators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='showpublication',
            name='show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='venue.Show'),
        ),
        migrations.AlterField(
            model_name='showpublication',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Créé'), (1, 'En vente'), (2, 'Vente terminée')], default=0),
        ),
    ]
