# Generated by Django 4.0.3 on 2022-05-19 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0035_condition_sparepart_suppliercompany_sparepartuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparepartuser',
            name='engineer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Назначить на'),
        ),
    ]
