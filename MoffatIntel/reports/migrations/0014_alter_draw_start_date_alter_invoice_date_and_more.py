# Generated by Django 4.1.6 on 2023-05-19 23:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_invoice_signed_alter_draw_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draw',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 17, 42, 8, 360383), verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 17, 42, 8, 360383), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 17, 42, 8, 360383), verbose_name='Invoice Date'),
        ),
    ]