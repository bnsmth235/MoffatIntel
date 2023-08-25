from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Project, Draw, Group, Subgroup, Subcontractor, Vendor, Report, Invoice, Check, Contract, Exhibit, \
    Estimate, ExhibitLineItem
from ..pdf_create.create_draw_report_by_sub import create_draw_report_by_sub

@login_required(login_url='projectmanagement:login')
def reports(request):
    reports = Report.objects.order_by('-name')
    projects = Project.objects.order_by('-name')
    draws = Draw.objects.order_by("id")
    groups = Group.objects.order_by("name")
    subgroups = Subgroup.objects.order_by("name")
    subs = Subcontractor.objects.order_by("name")
    vendors = Vendor.objects.order_by("name")
    exhibits = Exhibit.objects.order_by("id")
    invoices = Invoice.objects.order_by("id")
    checks = Check.objects.order_by("id")

    context = {
        'reports': reports,
        'projects': projects,
        'draws': draws,
        'groups': groups,
        'subgroups': subgroups,
        'subs': subs,
        'vendors': vendors,
        'exhibits': exhibits,
        'invoices': invoices,
        'checks': checks
    }

    return render(request, 'reports/all_reports.html', context)


@login_required(login_url='projectmanagement:login')
def new_draw_report_by_sub(request, project, sub):
    project = get_object_or_404(Project, pk=project)
    sub = None
    vendor = None
    checks = None
    invoices = None

    try:
        sub = get_object_or_404(Subcontractor, pk=sub)
    except:
        vendor = get_object_or_404(Vendor, pk=sub)

    if sub:
        invoices = Invoice.objects.filter(sub=sub)
        checks = Check.objects.filter(invoice__in=invoices)
    elif vendor:
        invoices = Invoice.objects.filter(vendor=vendor)
        checks = Check.objects.filter(invoice__in=invoices)
    else:
        redirect('projectmanagement:reports')

    exhibits = Exhibit.objects.filter(project=project, sub=sub)
    groups = Group.objects.filter(project=project)
    draws = Draw.objects.filter(project=project)
    line_items = ExhibitLineItem.objects.filter(exhibit__in=exhibits)

    report = create_draw_report_by_sub(project, draws, sub, vendor, checks, invoices, exhibits, line_items, groups)
    pdf_bytes = report.pdf.read()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{report.pdf.name}"'

    return response


