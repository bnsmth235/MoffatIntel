# Generated by Django 4.2.6 on 2024-06-06 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanagement', '0008_estimate_category_estimate_csi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimate',
            name='category',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='category',
        ),
        migrations.RemoveField(
            model_name='masterestimate',
            name='category',
        ),
        migrations.RemoveField(
            model_name='subcontractor',
            name='category',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='category',
        ),
        migrations.AlterField(
            model_name='estimate',
            name='csi',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='csi',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='masterestimate',
            name='csi',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='csi',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='csi',
            field=models.CharField(max_length=6),
        ),
    ]
