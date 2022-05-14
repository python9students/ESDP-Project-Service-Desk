# Generated by Django 4.0.3 on 2022-05-14 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0029_alter_ticket_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'permissions': [('see_engineer_tickets', 'Может видеть только заявки со статусами Назначенный, На исполнении, Исполненный'), ('see_chief_tickets', 'Может видеть заявки со всеми статусами'), ('close_ticket', 'Может закрывать заявки')], 'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
    ]
