# Generated by Django 4.0.3 on 2022-05-20 08:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0036_alter_sparepartuser_engineer'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparepartuser',
            name='assigned_by',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_spare_parts', to=settings.AUTH_USER_MODEL, verbose_name='Назначен кем'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sparepartuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 5, 20, 8, 27, 6, 574484, tzinfo=utc), verbose_name='Дата назначения запчасти'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sparepart',
            name='engineers',
            field=models.ManyToManyField(related_name='spare_parts', through='ticket.SparePartUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
