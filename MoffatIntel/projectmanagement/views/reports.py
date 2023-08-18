from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import Project, Draw, Group, Subgroup, Subcontractor, Vendor, Report, Invoice, Check, Contract, Exhibit, Estimate


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
