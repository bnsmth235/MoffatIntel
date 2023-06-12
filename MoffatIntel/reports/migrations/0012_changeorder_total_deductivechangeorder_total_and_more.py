# Generated by Django 4.1.6 on 2023-06-10 01:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_rename_sub_invoice_sub_id_alter_draw_start_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='changeorder',
            name='total',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='deductivechangeorder',
            name='total',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='draw',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 9, 19, 54, 3, 303588), verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 9, 19, 54, 3, 303588), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 9, 19, 54, 3, 303588), verbose_name='Invoice Date'),
        ),
    ]