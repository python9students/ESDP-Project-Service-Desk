# Generated by Django 4.0.3 on 2022-06-14 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0045_alter_sparepart_serial_number'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sparepart',
            unique_together={('serial_number',)},
        ),
    ]
