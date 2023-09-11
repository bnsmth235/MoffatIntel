import os
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from django.utils.baseconv import base64
from django.views.decorators.csrf import csrf_protect

from ..models import Project, Estimate, DIVISION_CHOICES, Subcontractor, Vendor, Group, Subgroup, EstimateLineItem
from ..pdf_create.create_estimate import create_estimate


@login_required(login_url='projectmanagement:login')
@csrf_protect
def all_estimates(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    estimates = Estimate.objects.filter(project_id = project).order_by('csi')
    subs = Subcontractor.objects.order_by('-name')
    vendors = Vendor.objects.order_by('name')

    context = {
        'subs': subs,
        'vendors': vendors,
        'project': project,
        'estimates': estimates,
        'divisions': DIVISION_CHOICES,
    }

    return render(request, 'estimates/all_estimates.html', context)


@login_required(login_url='projectmanagement:login')
@csrf_protect
def delete_estimate(request, estimate_id):
    estimate = get_object_or_404(Estimate, pk=estimate_id)
    project = estimate.project_id
    project.edited_by = request.user.username
    project.date = datetime.now()
    project.save()

    username = request.POST.get('username')
    print("Attempting to delete")

    if username == request.user.username:
        if os.path.exists(estimate.pdf.path):
            time.sleep(3)
            os.remove(estimate.pdf.path)
            estimate.delete()

    return redirect('projectmanagement:all_estimates', project_id=project.id)


@login_required(login_url='projectmanagement:login')
@csrf_protect
def estimate_pdf_view(request, estimate_id):
    estimate = get_object_or_404(Estimate, pk=estimate_id)
    pdf_bytes = estimate.pdf.read()
    pdf_data = base64.b64encode(pdf_bytes).decode('utf-8')
    return render(request, 'estimates/estimate_pdf_view.html', {'pdf_data': pdf_data, 'estimate': estimate})

@login_required(login_url='projectmanagment:login')
def generate_estimate(request, project_id, sub_id):
    project = get_object_or_404(Project, pk=project_id)
    groups = Group.objects.filter(project_id=project)
    subgroups = Subgroup.objects.filter(group_id__in=groups)

    sub = None
    vendor = None
    try:
        sub = get_object_or_404(Subcontractor, pk=sub_id)
    except:
        vendor = get_object_or_404(Vendor, pk=sub_id)

    context = {
        'project': project,
        'sub': sub,
        'vendor': vendor,
        'groups': groups,
        'subgroups': subgroups,
    }

    if request.method == 'POST':
        estimate = Estimate()
        estimate.date = datetime.now()
        estimate.project_id = project
        if sub:
            estimate.sub_id = sub
            estimate.vendor_id = None
        else:
            estimate.vendor_id = sub
            estimate.sub_id = None

        line_items = process_form_data(request)
        for line_item in line_items:
            line_item.project_id = project
            try:
                line_item.sub_id = sub
                line_item.vendor_id = None
            except:
                line_item.vendor_id = sub
                line_item.sub_id = None
            line_item.estimate_id = estimate
            line_item.save()

        estimate = create_estimate(estimate, line_items, project, sub, vendor)



    return render(request, 'estimates/generate_estimate.html', context)


def process_form_data(request):
    grouped_data = []
    line_items = []
    current_group = None

    for key, values in request.POST.lists():
        if key.startswith('group'):
            group_index = int(key[5:])
            current_group = {'group': values[0], 'rows': []}
            grouped_data.append(current_group)
        elif key.startswith('subgroup'):
            if current_group is not None:
                current_group['subgroup'] = values[0]
        elif key.startswith('scope'):
            if current_group is not None:
                row_index = int(key.split('[')[2].split(']')[0])
                row_data = {
                    'scope': values[0],
                    'qty': request.POST.get(f'qty[{group_index}][{row_index}]'),
                    'unitPrice': request.POST.get(f'unitprice[{group_index}][{row_index}]'),
                    'totalPrice': request.POST.get(f'totalprice[{group_index}][{row_index}]'),
                }
                current_group['rows'].append(row_data)

    for group in grouped_data:
        for row in group['rows']:
            line_item = EstimateLineItem()

            # Convert the string IDs to integers using int()
            try:
                group_id = int(group.get('group'))
            except:
                group_id = None
            try:
                subgroup_id = int(group.get('subgroup'))
            except:
                subgroup_id = None

            # Set the group_id and subgroup_id fields
            line_item.group_id = get_object_or_404(Group, id=group_id) if group_id else None
            line_item.subgroup_id = get_object_or_404(Subgroup, id=subgroup_id)if subgroup_id else None

            # Set the remaining fields
            line_item.project_id_id = 1
            line_item.sub_id_id = 1
            line_item.vendor_id_id = 1
            line_item.scope = row['scope']
            line_item.qty = row['qty']
            line_item.unit_price = row['unitPrice']
            line_item.total = float(line_item.qty) * float(line_item.unit_price)

            line_items.append(line_item)

    return line_items