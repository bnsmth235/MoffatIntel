# Generated by Django 4.1.6 on 2023-09-13 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanagement', '0004_estimate_vendor_id_alter_estimate_sub_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimatelineitem',
            name='estimate_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.estimate'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estimatelineitem',
            name='qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='estimatelineitem',
            name='total',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='estimatelineitem',
            name='unit_price',
            field=models.FloatField(default=0),
        ),
    ]