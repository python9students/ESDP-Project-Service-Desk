# Generated by Django 4.0.3 on 2022-05-25 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0039_alter_sparepartuser_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='expected_finish_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='Ожидаемая дата завершения'),
        ),
    ]
