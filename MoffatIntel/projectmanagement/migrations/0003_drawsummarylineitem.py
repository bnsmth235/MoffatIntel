# Generated by Django 4.2.6 on 2024-06-14 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanagement', '0002_populate'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrawSummaryLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draw_amount', models.FloatField(default=0.0)),
                ('description', models.CharField(max_length=250)),
                ('draw_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.draw')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
            ],
        ),
    ]