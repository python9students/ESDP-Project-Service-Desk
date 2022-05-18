# Generated by Django 4.0.3 on 2022-05-18 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0013_alter_user_first_name_alter_user_last_name'),
        ('ticket', '0034_remove_contract_current_document_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Состояние')),
            ],
            options={
                'verbose_name': 'Состояние запчасти',
                'verbose_name_plural': 'Состояние запчастей',
                'db_table': 'spare_part_condition',
            },
        ),
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=100, unique=True, verbose_name='Серийный №')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('product_code', models.CharField(max_length=100, verbose_name='Код продукта')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('measure_unit', models.CharField(choices=[('pc', 'шт'), ('unit', 'узел')], default='шт', max_length=20, verbose_name='Единица измерения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления запчасти')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.condition', verbose_name='Состояние запчасти')),
            ],
            options={
                'verbose_name': 'Запчасть',
                'verbose_name_plural': 'Запчасти',
                'db_table': 'spare_part',
            },
        ),
        migrations.CreateModel(
            name='SupplierCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Компания поставщик')),
            ],
            options={
                'verbose_name': 'Компания поставщик',
                'verbose_name_plural': 'Компании поставщики',
                'db_table': 'spare_part_supplier_company',
            },
        ),
        migrations.CreateModel(
            name='SparePartUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('engineer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Работник')),
                ('spare_part', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticket.sparepart', verbose_name='Запчасть')),
            ],
            options={
                'verbose_name': 'Передача запчасти инженеру',
                'verbose_name_plural': 'Передача запчастей инженеру',
                'db_table': 'Spare_part_user',
            },
        ),
        migrations.AddField(
            model_name='sparepart',
            name='engineers',
            field=models.ManyToManyField(related_name='spare_part', through='ticket.SparePartUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sparepart',
            name='supplier_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.suppliercompany', verbose_name='Компания поставщик'),
        ),
    ]
