# Generated by Django 4.0.3 on 2022-05-05 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0023_contractstatus_contracttype_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='time_to_fix_problem_SLA',
            field=models.DurationField(blank=True, default=None, null=True, verbose_name='Время на устранение проблемы'),
        ),
    ]
