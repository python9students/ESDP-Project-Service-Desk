# Generated by Django 4.0.3 on 2022-04-18 16:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_alter_client_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='website',
            field=models.URLField(blank=True, max_length=255, validators=[django.core.validators.RegexValidator('[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)')], verbose_name='Вебсайт'),
        ),
    ]
