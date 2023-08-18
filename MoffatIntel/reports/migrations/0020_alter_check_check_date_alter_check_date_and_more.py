# Generated by Django 4.1.6 on 2023-08-15 18:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0019_remove_invoice_lien_release_pdf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='check_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 12, 21, 33, 830526), verbose_name='Check Date'),
        ),
        migrations.AlterField(
            model_name='check',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 12, 21, 33, 830526), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='check',
            name='signed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='draw',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 12, 21, 33, 829526), verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 12, 21, 33, 829526), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 12, 21, 33, 829526), verbose_name='Invoice Date'),
        ),
    ]