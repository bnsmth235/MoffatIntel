# Generated by Django 4.1.6 on 2023-08-15 20:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0020_alter_check_check_date_alter_check_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('total', models.FloatField(default=0.0)),
                ('csi', models.CharField(choices=[('1', 'General Requirement'), ('2', 'Site Works'), ('3', 'Concrete'), ('4', 'Masonry'), ('5', 'Metals'), ('6', 'Wood and Plastics'), ('7', 'Thermal and Moisture Protection'), ('8', 'Doors and Windows'), ('9', 'Finishes'), ('10', 'Specialties'), ('11', 'Equipment'), ('12', 'Furnishings'), ('13', 'Special Construction'), ('14', 'Conveying Systems'), ('15', 'Mechanical/Plumbing'), ('16', 'Electrical')], max_length=2)),
                ('category', models.CharField(choices=[('1', 'Civil Engineering'), ('2', 'Architecture'), ('3', 'Electrical Engineering'), ('4', 'Mechanical Engineering'), ('5', 'Plumbing'), ('6', 'Environmental'), ('7', 'Health Department'), ('8', 'Amenities'), ('9', 'Landscape')], max_length=50)),
                ('pdf', models.FileField(default=None, upload_to='static/reports/estimates/')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.project')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.subcontractor')),
            ],
        ),
        migrations.AlterField(
            model_name='check',
            name='check_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 14, 42, 4, 526709), verbose_name='Check Date'),
        ),
        migrations.AlterField(
            model_name='check',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 14, 42, 4, 526709), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='draw',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 14, 42, 4, 526709), verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 14, 42, 4, 526709), verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 14, 42, 4, 526709), verbose_name='Invoice Date'),
        ),
        migrations.DeleteModel(
            name='Proposal',
        ),
    ]