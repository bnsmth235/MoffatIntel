# Generated by Django 4.1.6 on 2023-08-16 20:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0025_alter_check_check_date_alter_check_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='group_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.group'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='subgroup_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.subgroup'),
        ),
        migrations.AlterField(
            model_name='check',
            name='check_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 16, 14, 19, 9, 613002), verbose_name='Check Date'),
        ),
        migrations.AlterField(
            model_name='check',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 16, 14, 19, 9, 613002), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='draw',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 16, 14, 19, 9, 613002), verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 16, 14, 19, 9, 613002), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 16, 14, 19, 9, 613002), verbose_name='Invoice Date'),
        ),
    ]