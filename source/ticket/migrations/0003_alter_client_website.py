# Generated by Django 4.0.3 on 2022-04-17 13:08

from django.db import migrations, models
import ticket.views.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_rename_service_object_serviceobject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='website',
            field=models.URLField(blank=True, max_length=255, validators=[ticket.views.validators.OptionalSchemeURLValidator], verbose_name='Вебсайт'),
        ),
    ]