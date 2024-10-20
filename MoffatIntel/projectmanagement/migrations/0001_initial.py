# Generated by Django 4.1.6 on 2023-09-13 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('num', models.IntegerField(default=1)),
                ('edited_by', models.CharField(max_length=20)),
                ('start_date', models.DateTimeField(verbose_name='Start Date')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('edited_by', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('I', 'In Progress'), ('C', 'Completed'), ('O', 'On Hold')], max_length=1)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zip', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Subcontractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('w9', models.CharField(max_length=20)),
                ('csi', models.CharField(choices=[('1', 'General Requirement'), ('2', 'Site Works'), ('3', 'Concrete'), ('4', 'Masonry'), ('5', 'Metals'), ('6', 'Wood and Plastics'), ('7', 'Thermal and Moisture Protection'), ('8', 'Doors and Windows'), ('9', 'Finishes'), ('10', 'Specialties'), ('11', 'Equipment'), ('12', 'Furnishings'), ('13', 'Special Construction'), ('14', 'Conveying Systems'), ('15', 'Mechanical/Plumbing'), ('16', 'Electrical')], max_length=2)),
                ('category', models.CharField(choices=[('1', 'Civil Engineering'), ('2', 'Architecture'), ('3', 'Electrical Engineering'), ('4', 'Mechanical Engineering'), ('5', 'Plumbing'), ('6', 'Environmental'), ('7', 'Health Department'), ('8', 'Amenities'), ('9', 'Landscape')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('cname', models.CharField(default='', max_length=50)),
                ('cphone', models.CharField(default='', max_length=11)),
                ('cemail', models.EmailField(default='', max_length=254)),
                ('w9', models.CharField(max_length=20)),
                ('csi', models.CharField(choices=[('1', 'General Requirement'), ('2', 'Site Works'), ('3', 'Concrete'), ('4', 'Masonry'), ('5', 'Metals'), ('6', 'Wood and Plastics'), ('7', 'Thermal and Moisture Protection'), ('8', 'Doors and Windows'), ('9', 'Finishes'), ('10', 'Specialties'), ('11', 'Equipment'), ('12', 'Furnishings'), ('13', 'Special Construction'), ('14', 'Conveying Systems'), ('15', 'Mechanical/Plumbing'), ('16', 'Electrical')], max_length=2)),
                ('category', models.CharField(choices=[('1', 'Civil Engineering'), ('2', 'Architecture'), ('3', 'Electrical Engineering'), ('4', 'Mechanical Engineering'), ('5', 'Plumbing'), ('6', 'Environmental'), ('7', 'Health Department'), ('8', 'Amenities'), ('9', 'Landscape')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SWO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('description', models.CharField(default='', max_length=200)),
                ('total', models.FloatField()),
                ('pdf', models.FileField(upload_to='projectmanagement/SWOs')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
            ],
        ),
        migrations.CreateModel(
            name='Subgroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.group')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('order_number', models.CharField(max_length=50)),
                ('date', models.DateTimeField(verbose_name='Order Date')),
                ('total', models.FloatField(default=0.0)),
                ('pdf', models.FileField(upload_to='projectmanagement/purchase_orders')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('vendor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('edited_by', models.CharField(max_length=20)),
                ('pdf', models.FileField(default=None, upload_to='projectmanagement/plans/')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('invoice_date', models.DateTimeField(verbose_name='Invoice Date')),
                ('invoice_num', models.CharField(default='', max_length=20)),
                ('csi', models.CharField(choices=[('1', 'General Requirement'), ('2', 'Site Works'), ('3', 'Concrete'), ('4', 'Masonry'), ('5', 'Metals'), ('6', 'Wood and Plastics'), ('7', 'Thermal and Moisture Protection'), ('8', 'Doors and Windows'), ('9', 'Finishes'), ('10', 'Specialties'), ('11', 'Equipment'), ('12', 'Furnishings'), ('13', 'Special Construction'), ('14', 'Conveying Systems'), ('15', 'Mechanical/Plumbing'), ('16', 'Electrical')], max_length=50)),
                ('category', models.CharField(choices=[('1', 'Civil Engineering'), ('2', 'Architecture'), ('3', 'Electrical Engineering'), ('4', 'Mechanical Engineering'), ('5', 'Plumbing'), ('6', 'Environmental'), ('7', 'Health Department'), ('8', 'Amenities'), ('9', 'Landscape')], max_length=50)),
                ('method', models.CharField(choices=[('I', 'Invoice'), ('E', 'Exhibit'), ('P', 'Purchase Order')], default='I', max_length=1)),
                ('invoice_total', models.FloatField(default=0.0)),
                ('description', models.TextField()),
                ('invoice_pdf', models.FileField(default=None, upload_to='projectmanagement/invoices/')),
                ('draw_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.draw')),
                ('group_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.group')),
                ('sub_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
                ('subgroup_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subgroup')),
                ('vendor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.vendor')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project'),
        ),
        migrations.CreateModel(
            name='ExhibitLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope', models.CharField(max_length=500)),
                ('qty', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('total', models.FloatField()),
                ('group_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.group')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('sub_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
                ('subgroup_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subgroup')),
                ('vendor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Exhibit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('total', models.FloatField(default=0.0)),
                ('pdf', models.FileField(default=None, upload_to='projectmanagement/exhibits/')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
            ],
        ),
        migrations.CreateModel(
            name='EstimateLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope', models.CharField(max_length=500)),
                ('qty', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('total', models.FloatField()),
                ('group_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.group')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('sub_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
                ('subgroup_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subgroup')),
                ('vendor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('total', models.FloatField(default=0.0)),
                ('csi', models.CharField(choices=[('1', 'General Requirement'), ('2', 'Site Works'), ('3', 'Concrete'), ('4', 'Masonry'), ('5', 'Metals'), ('6', 'Wood and Plastics'), ('7', 'Thermal and Moisture Protection'), ('8', 'Doors and Windows'), ('9', 'Finishes'), ('10', 'Specialties'), ('11', 'Equipment'), ('12', 'Furnishings'), ('13', 'Special Construction'), ('14', 'Conveying Systems'), ('15', 'Mechanical/Plumbing'), ('16', 'Electrical')], max_length=2)),
                ('category', models.CharField(choices=[('1', 'Civil Engineering'), ('2', 'Architecture'), ('3', 'Electrical Engineering'), ('4', 'Mechanical Engineering'), ('5', 'Plumbing'), ('6', 'Environmental'), ('7', 'Health Department'), ('8', 'Amenities'), ('9', 'Landscape')], max_length=50)),
                ('pdf', models.FileField(default=None, upload_to='projectmanagement/estimates/')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
            ],
        ),
        migrations.AddField(
            model_name='draw',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project'),
        ),
        migrations.CreateModel(
            name='DeductiveChangeOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=50)),
                ('date', models.DateTimeField(verbose_name='Order Date')),
                ('total', models.FloatField(default=0.0)),
                ('pdf', models.FileField(upload_to='projectmanagement/deductive_change_orders')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('description', models.CharField(default='', max_length=200)),
                ('total', models.FloatField()),
                ('pdf', models.FileField(upload_to='projectmanagement/contracts')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Last Modified')),
                ('check_date', models.DateTimeField(verbose_name='Check Date')),
                ('check_num', models.IntegerField()),
                ('check_total', models.FloatField(default=0.0)),
                ('distributed', models.CharField(max_length=50)),
                ('check_pdf', models.FileField(default=None, upload_to='projectmanagement/checks/')),
                ('lien_release_type', models.CharField(choices=[('F', 'Final'), ('C', 'Conditional'), ('N', 'N/A')], default='N', max_length=20)),
                ('lien_release_pdf', models.FileField(default=None, upload_to='projectmanagement/lien_releases')),
                ('signed', models.BooleanField(default=False)),
                ('invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=50)),
                ('date', models.DateTimeField(verbose_name='Order Date')),
                ('total', models.FloatField(default=0.0)),
                ('pdf', models.FileField(upload_to='projectmanagement/change_orders')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.project')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanagement.subcontractor')),
            ],
        ),
    ]
