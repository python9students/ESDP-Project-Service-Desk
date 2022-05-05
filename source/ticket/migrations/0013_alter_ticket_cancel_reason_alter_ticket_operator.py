# Generated by Django 4.0.3 on 2022-04-29 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0012_alter_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='cancel_reason',
            field=models.CharField(max_length=255, verbose_name='Причина отмены заявки'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='operator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operator_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Оператор'),
        ),
    ]