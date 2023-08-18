# Generated by Django 4.1.6 on 2023-08-18 13:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0027_draw_num_alter_check_check_date_alter_check_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changeorder',
            name='pdf',
            field=models.FileField(upload_to='reports/change_orders'),
        ),
        migrations.AlterField(
            model_name='check',
            name='check_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 18, 7, 34, 49, 928813), verbose_name='Check Date'),
        ),
        migrations.AlterField(
            model_name='check',
            name='check_pdf',
            field=models.FileField(default=None, upload_to='reports/checks/'),
        ),
        migrations.AlterField(
            model_name='check',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 18, 7, 34, 49, 928813), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='check',
            name='lien_release_pdf',
            field=models.FileField(default=None, upload_to='reports/lien_releases'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='pdf',
            field=models.FileField(upload_to='reports/contracts'),
        ),
        migrations.AlterField(
            model_name='deductivechangeorder',
            name='pdf',
            field=models.FileField(upload_to='reports/deductive_change_orders'),
        ),
        migrations.AlterField(
            model_name='draw',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 18, 7, 34, 49, 928813), verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='pdf',
            field=models.FileField(default=None, upload_to='reports/estimates/'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='pdf',
            field=models.FileField(default=None, upload_to='reports/exhibits/'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 18, 7, 34, 49, 928813), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 18, 7, 34, 49, 928813), verbose_name='Invoice Date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_pdf',
            field=models.FileField(default=None, upload_to='reports/invoices/'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='pdf',
            field=models.FileField(default=None, upload_to='reports/plans/'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='pdf',
            field=models.FileField(upload_to='reports/purchase_orders'),
        ),
        migrations.AlterField(
            model_name='swo',
            name='pdf',
            field=models.FileField(upload_to='reports/SWOs'),
        ),
    ]
