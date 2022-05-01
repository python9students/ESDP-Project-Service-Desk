# Generated by Django 4.0.3 on 2022-05-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0017_alter_ticket_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Область',
                'verbose_name_plural': 'Области',
                'db_table': 'region',
            },
        ),
    ]
