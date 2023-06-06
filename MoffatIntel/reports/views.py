import os
from io import BytesIO

from PyPDF2.generic import NameObject
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.db.models import Sum
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth import authenticate, logout, login
import base64
import PyPDF2
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import datetime
from django.core.files.uploadedfile import UploadedFile

from .forms import DocumentForm, InvoiceForm
from .models import *



STATE_OPTIONS = [
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
]

STATUS_OPTIONS = [("I", "In Progress"), ("C", "Completed"), ("O", "On Hold")]

METHOD_OPTIONS = [("I", "Invoice"), ("E", "Exhibit"), ("P", "Purchase Order")]

LIEN_RELEASE_OPTIONS = [("F", "Final"), ("C", "Conditional"), ("N", "N/A")]


@ensure_csrf_cookie
def index(request):
    username = ""
    password = ""
    user = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = request.POST.get('refresh', None)
            if refresh:
                return redirect(request.path)
            else:
                redirect_url = request.POST.get('next', None)
                if redirect_url:
                    return redirect(resolve_url(redirect_url))
                else:
                    return redirect('reports:home')
        else:
            if (username == "" and password == ""):
                return render(request, 'reports/login.html', {'error_message': "Please input login credentials"})
            else:
                return render(request, 'reports/login.html',
                              {'error_message': "The provided credentials are incorrect"})
    else:
        return render(request, 'reports/login.html')


def log_out(request):
    logout(request)
    return render(request, 'reports/login.html')


@login_required(login_url='reports:login')
def input_data(request):
    return render(request, 'reports/input_data.html')


@login_required(login_url='reports:login')
def edit_sub(request, sub_id):
    sub = get_object_or_404(Subcontractor, pk=sub_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        w9 = request.POST.get('w9')
        if not name:
            return render(request, 'reports/edit_sub.html', {'error_message': "Please enter the subcontractor name. (Less than 50 characters)", 'sub': sub})

        if not address and not phone and not email:
            return render(request, 'reports/all_subs.html', {'error_message': "Please enter at least one form of contact", 'sub': sub})

        sub.name = name
        sub.addresss = address
        sub.phone = phone
        sub.email = email
        sub.w9 = w9

        sub.save()

        return redirect('reports:all_subs')

    return render(request, 'reports/edit_sub.html', {'sub': sub})


@login_required(login_url='reports:login')
def delete_sub(request, sub_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        print("Attempting to delete")

        if username == request.user.username:
            sub = get_object_or_404(Subcontractor, pk=sub_id)
            sub.delete()
            print("Subcontractor deleted")
        else:
            print("Username incorrect")

    return redirect('reports:all_subs')


@login_required(login_url='reports:login')
def sub_select(request, project_id):
    subs = Subcontractor.objects.order_by("name")
    project = get_object_or_404(Project, pk=project_id)

    return render(request, 'reports/sub_select.html', {'subs': subs, 'project': project})

@login_required(login_url='reports:login')
def all_subs(request):
    subs = Subcontractor.objects.order_by("name")
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        w9 = request.POST.get('w9')

        if not name:
            return render(request, 'reports/all_subs.html', {'error_message': "Please enter the subcontractor name. (Less than 50 characters)"})

        if not address and not phone and not email:
            return render(request, 'reports/all_subs.html', {'error_message': "Please enter at least one form of contact"})

        sub = Subcontractor()
        sub.name = name
        sub.address = address
        sub.phone = phone
        sub.email = email
        sub.w9 = w9
        sub.save()

        return redirect(reverse('reports:all_subs'))

    return render(request, 'reports/all_subs.html', {'subs': subs})


@login_required(login_url='reports:login')
def home(request):
    recent_projects = Project.objects.order_by('-date', '-status')[:5]
    context = {'recent_projects': recent_projects}
    return render(request, 'reports/home.html', context)


@login_required(login_url='reports:login')
def all(request):
    projects = Project.objects.order_by('-date', '-status')
    context = {'projects': projects}
    return render(request, 'reports/all_proj.html', context)


@login_required(login_url='reports:login')
def new_proj(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        date = datetime.datetime.now()
        edited_by = request.user.username
        status = "I"

        if not name or not address or not city or not state or not zip:
            return render(request, 'reports/new_proj.html', {'error_message': "Please fill out all fields",
                                                             'state_options': STATE_OPTIONS})

        if int(zip) < 10000 and zip != "":
            return render(request, 'reports/new_proj.html', {'error_message': "Zip code incorrect",
                                                             'state_options': STATE_OPTIONS})

        project = Project(name=name, date=date, edited_by=edited_by, status=status,
                           address=address, city=city, state=state, zip=zip)
        project.save()
        print("Project " + project.name + " has been saved")

        return redirect('reports:home')

    return render(request, 'reports/new_proj.html', {"state_options": STATE_OPTIONS})

@login_required(login_url='reports:login')
def new_contract(request):
    projects = Project.objects.order_by('name')
    subs = Subcontractor.objects.order_by('name')

    context = {'projects': projects, 'subs': subs}

    if request.method == 'POST':
        project = get_object_or_404(Project, pk=request.POST.get('project'))
        sub = get_object_or_404(Subcontractor, pk=request.POST.get('sub'))
        contract_date = request.POST.get('contract_date')
        description = request.POST.get('description')
        contract_total = request.POST.get('contract_total')
        p_and_p = bool(request.POST.get('p_and_p'))
        guarantor = bool(request.POST.get('guarantor'))
        payroll_cert = bool(request.POST.get('payroll_cert'))
        complete_drawings = bool(request.POST.get('complete_drawings'))
        o_and_m = bool(request.POST.get('o_and_m'))
        as_built = bool(request.POST.get('as_built'))
        manuals = bool(request.POST.get('manuals'))
        listed_in_subcontract = bool(request.POST.get('listed_in_subcontract'))
        listed_in_exhibit = bool(request.POST.get('listed_in_exhibit'))
        offsite_disposal = bool(request.POST.get('offsite_disposal'))
        onsite_dumpster_sub_pay = bool(request.POST.get('onsite_dumpster_sub_pay'))
        onsite_dumpster = bool(request.POST.get('onsite_dumpster'))

        context.update({
            'failure': True,
            'projectselect': project,
            'subselect': sub,
            'contract_date': contract_date,
            'description': description,
            'contract_total': contract_total,
            'p_and_p': p_and_p,
            'guarantor': guarantor,
            'payroll_cert': payroll_cert,
            'complete_drawings': complete_drawings,
            'o_and_m': o_and_m,
            'as_built': as_built,
            'manuals': manuals,
            'listed_in_subcontract': listed_in_subcontract,
            'listed_in_exhibit': listed_in_exhibit,
            'offsite_disposal': offsite_disposal,
            'onsite_dumpster_sub_pay': onsite_dumpster_sub_pay,
            'onsite_dumpster': onsite_dumpster,
        })

        if not project or not sub or not description or not contract_total or not contract_date:
            context.update({'error_message': "Please fill out all fields as specified (missing req data)"})
            return render(request, 'reports/new_contract.html', context)

        if listed_in_exhibit == listed_in_subcontract:
            context.update({'error_message': "Please fill out all fields as specified (sub/exhibit)"})
            return render(request, 'reports/new_contract.html', context)

        if (offsite_disposal + onsite_dumpster + onsite_dumpster_sub_pay) != 1:
            context.update({'error_message': "Please fill out all fields as specified (disposal)"})
            return render(request, 'reports/new_contract.html', context)

        if not project in projects or not sub in subs:
            context.update({'error_message': "Please pick an existing Project and Subcontractor"})
            return render(request, 'reports/new_contract.html', context)

        try:
            contract_total = float(contract_total)
            if contract_total < 0:
                raise
        except:
            context.update({'error_message': "Contract total must be a positive number"})
            return render(request, 'reports/new_contract.html', context)

        contract = Contract()
        contract.date = contract_date
        contract.total = contract_total
        contract.sub_id = sub
        contract.description = description[:196]+"..."
        contract.project_id = project

        file_path = os.path.join(settings.STATIC_ROOT, 'reports\pdf_templates\contract_template.pdf')

        output_path = sub.name + " Contract " + contract_date

        if os.path.exists(output_path + ".pdf"):
            counter = 1
            while os.path.exists(output_path + "("+str(counter)+")" + ".pdf"):
                counter += 1
            output_path += "("+str(counter)+")"

        output_path += ".pdf"

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                input_pdf = PyPDF2.PdfReader(file)
                output_pdf = PyPDF2.PdfWriter()

                fields = input_pdf.get_fields()
                print(fields)

                for field in fields:
                    default = ''
                    try:
                        if fields[field]['/DV'] != "":
                            default = fields[field]['/DV']
                        fields[field] = default
                    except:
                        fields[field] = ''

                fields['sub_name'] = sub.name
                fields['sub_address'] = sub.address
                fields['job_number'] = project.id
                fields['contract_date'] = contract_date
                fields['project_name'] = project.name
                fields['project_address'] = project.address
                fields['project_city_state_zip'] = project.city + ", " + project.state + ", " + str(project.zip)
                fields['contract_num'] = len(Contract.objects.all()) + 1
                fields['sub_w9'] = sub.w9
                fields['description'] = description
                fields['contract_total'] = "$" + "{:.2f}".format(contract_total)

                fields['p_and_p_req'] = NameObject("/0") if p_and_p else "/Off"
                fields['p_and_p_no_req'] = NameObject("/0") if not p_and_p else "/Off"
                fields['guarantor_req'] = NameObject("/0") if guarantor else "/Off"
                fields['guarantor_no_req'] = NameObject("/0") if not guarantor else "/Off"
                fields['payroll_cert_req'] = NameObject("/0") if payroll_cert else "/Off"
                fields['payroll_cert_no_req'] = NameObject("/0") if not payroll_cert else "/Off"
                fields['complete_drawings'] = NameObject("/0") if complete_drawings else "/Off"
                fields['o_and_m'] = NameObject("/0") if o_and_m else "/Off"
                fields['as_built'] = NameObject("/0") if as_built else "/Off"
                fields['manuals'] = NameObject("/0") if manuals else "/Off"
                fields['drawings_no_req'] = NameObject("/0") if not complete_drawings and not o_and_m and not as_built and not manuals else "\Off"
                fields['listed_in_subcontract'] = NameObject("/0") if listed_in_subcontract else "/Off"
                fields['listed_in_exhibit'] = NameObject("/0") if listed_in_exhibit else "/Off"
                fields['offsite_disposal'] = NameObject("/0") if offsite_disposal else "/Off"
                fields['onsite_dumpster_sub_pay'] = NameObject("/0") if onsite_dumpster_sub_pay else "/Off"
                fields['onsite_dumpster'] = NameObject("/0") if onsite_dumpster else "/Off"

                for page_num in range(input_pdf._get_num_pages()):
                    page = input_pdf._get_page(page_num)
                    output_pdf.add_page(page)
                    output_pdf.update_page_form_field_values(output_pdf.get_page(page_num), fields)

                with BytesIO() as output_buffer:
                    output_pdf.write(output_buffer)

                    # Set the file pointer to the beginning of the BytesIO object
                    output_buffer.seek(0)

                    # Create a Django File object from the BytesIO object
                    contract_pdf = File(output_buffer, name=output_path)

                    # Assign the File object to the pdf field of the Contract model
                    contract.pdf = contract_pdf
                    contract.save()

                project.date = datetime.datetime.now()
                project.edited_by = request.user.username
                project.save()

        else:
            print("file path :" + file_path +"does not exist")

        return redirect('reports:contract_view', project_id=project.id, sub_id=sub.id)

    return render(request, 'reports/new_contract.html', context)


@login_required(login_url='reports:login')
def new_invoice(request, project_id, draw_id):
    project = get_object_or_404(Project, pk=project_id)
    draw = get_object_or_404(Draw, pk=draw_id)
    subs = Subcontractor.objects.order_by('name')
    invoice_form = InvoiceForm(request.POST, request.FILES)

    context = {
        'subs': subs,
        'project': project,
        'form': invoice_form,
        'draw': draw,
        'method_choices': METHOD_OPTIONS,
        'lien_release_type_choices': LIEN_RELEASE_OPTIONS
    }

    if request.method == 'POST':
        invoice_date = request.POST.get('invoice_date')
        invoice_num = request.POST.get('invoice_num')
        division_code = request.POST.get('division_code')
        method = request.POST.get('method')
        sub_name = request.POST.get('sub')
        sub = get_object_or_404(Subcontractor, name=sub_name)

        invoice_total = request.POST.get('invoice_total')

        description = request.POST.get('description')
        lien_release_type = request.POST.get('lien_release_type')
        w9 = request.POST.get('w9')
        signed = request.POST.get('signed', False)

        if not invoice_date or not invoice_num or not division_code or not method or not sub or not invoice_total or not description or not lien_release_type or not w9:
            context.update({'error_message': "Please fill out all fields"})
            return render(request, 'reports/new_invoice.html', context)

        if invoice_form.is_valid():
            invoice = Invoice()
            invoice.draw_id = draw
            invoice.invoice_date = invoice_date
            invoice.invoice_num = invoice_num
            invoice.division_code = division_code
            invoice.method = method
            invoice.sub = sub
            invoice.invoice_total = invoice_total
            invoice.description = description
            invoice.lien_release_type = lien_release_type
            invoice.w9 = w9
            invoice.signed = signed

            # Handle invoice PDF
            if 'invoice_pdf' in request.FILES:
                invoice.invoice_pdf = request.FILES['invoice_pdf']
                if not invoice.invoice_pdf.file.content_type.startswith('application/pdf'):
                    context.update({'error_message': "Only PDFs are allowed for the Invoice PDF"})
                    return render(request, 'reports/new_invoice.html', context)

            # Handle lien release PDF
            if 'lien_release_pdf' in request.FILES:
                invoice.lien_release_pdf = request.FILES['lien_release_pdf']
                if not invoice.lien_release_pdf.file.content_type.startswith('application/pdf'):
                    context.update({'error_message': "Only PDFs are allowed for the Lien Release PDF"})
                    return render(request, 'reports/new_invoice.html', context)

            else:
                invoice.signed = None;

            # Save invoice and related objects
            project.edited_by = request.user.username
            project.date = datetime.datetime.now()
            project.save()

            draw.edited_by = request.user.username
            draw.date = datetime.datetime.now()
            draw.save()

            invoice.save()

            return redirect('reports:draw_view', project_id=project_id, draw_id=draw_id)  # Redirect to a success page
        else:
            print(invoice_form.errors)
            context.update({'error_message': "File upload failed"})
            return render(request, 'reports/new_invoice.html', context)

    return render(request, 'reports/new_invoice.html', context)


@login_required(login_url='reports:login')
def new_draw(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    project.date = datetime.datetime.now()
    project.edited_by = request.user.username

    cur_draw = Draw(date=datetime.datetime.now(), project_id=project, edited_by=request.user.username)

    cur_draw.save()
    project.save()

    return all_draws(request, project_id)


@login_required(login_url='reports:login')
def todo(request):
    invoices = Invoice.objects.order_by("-invoice_date").filter(signed=False)

    context = {
        'invoices': invoices
    }

    return render(request, 'reports/todo.html', context)



@login_required(login_url='reports:login')
def add_signature(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    draw = get_object_or_404(Draw, pk=invoice.draw_id.id)
    project = get_object_or_404(Project, pk=draw.project_id.id)

    return edit_invoice(request, project.id, draw.id, invoice_id)

@login_required(login_url='reports:login')
def all_draws(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    draws = Draw.objects.order_by('-date').filter(project_id=project.id)

    context = {'draws': draws, 'project': project}

    return render(request, 'reports/all_draws.html', context)


@login_required(login_url='reports:login')
def edit_proj(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        status = request.POST.get('status')
        date = datetime.datetime.now()
        edited_by = request.user.username

        if not name or not address or not city or not state or not zip:
            return render(request, 'reports/edit_project.html', {'error_message': "Please fill out all fields",
                                                                 'state_options': STATE_OPTIONS,
                                                                 'status_options': STATUS_OPTIONS})

        if int(zip) < 10000 and zip != "":
            return render(request, 'reports/edit_project.html', {'error_message': "Zip code incorrect",
                                                                 'state_options': STATE_OPTIONS,
                                                                 'status_options': STATUS_OPTIONS})

        project.name = name
        project.address = address
        project.city = city
        project.state = state
        project.zip = zip
        project.status = status
        project.date = date
        project.edited_by = edited_by
        project.save()

        return redirect('reports:home')

    project.address = [x.strip() for x in project.address.split(',')]
    return render(request, 'reports/edit_project.html', {'project': project,
                                                         'state_options': STATE_OPTIONS,
                                                         'status_options': STATUS_OPTIONS})


@login_required(login_url='reports:login')
def delete_proj(request, project_id):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        username = request.POST.get('username')
        print("Attempting to delete")

        if username == request.user.username:
            project = get_object_or_404(Project, pk=project_id)
            project.delete()
            print("Project deleted")
        else:
            print("Username incorrect")

    return redirect('reports:home')


@login_required(login_url='reports:login')
def delete_draw(request, project_id):
    if request.method == 'POST':
        draw_id = request.POST.get('draw_id')
        username = request.POST.get('username')
        print("Attempting to delete draw " + draw_id)

        if username == request.user.username:
            cur_draw = get_object_or_404(Draw, pk=draw_id)
            cur_draw.delete()
            print("Draw deleted")
        else:
            print("Username incorrect")

    return redirect('reports:all_draws', project_id=project_id)


@login_required(login_url='reports:login')
def project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'reports/project_view.html', {'project': project})


@login_required(login_url='reports:login')
def all_plans(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = DocumentForm(request.POST, request.FILES)

    plans = Plan.objects.order_by('-date').filter(project_id=project.id)

    context = {'plans': plans, 'project': project, 'form': form}

    return render(request, 'reports/all_plans.html', context)


@login_required(login_url='reports:login')
def upload_plan(request, project_id):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file: UploadedFile = request.FILES['pdf']
            if uploaded_file.content_type != 'application/pdf':
                return render(request, 'reports/all_plans.html', {'project': get_object_or_404(Project, pk=project_id), 'form': form, 'error_message': "Only PDF's allowed."})

            plan = form.save(commit=False)
            name = request.POST.get('name')
            if not name:
                return render(request, 'reports/all_plans.html',
                              {'project': get_object_or_404(Project, pk=project_id), 'form': form,
                               'error_message': "Please enter a name for the plan."})

            plan.name = name;
            plan.edited_by = request.user.username
            plan.date = datetime.datetime.now()
            plan.project_id = get_object_or_404(Project, pk=project_id)
            plan.save()
            form.save_m2m()

            return redirect('reports:all_plans', project_id=project_id)
        else:
            return render(request, 'reports/all_plans.html', {'project': get_object_or_404(Project, pk=project_id), 'form': form, 'error_message': "File upload failed."})
    else:
        form = DocumentForm()

    return render(request, 'reports/all_plans.html', {'project': get_object_or_404(Project, pk=project_id), 'form': form})


@login_required(login_url='reports:login')
def delete_plan(request, project_id):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        print("Attempting to delete plan "+ plan_id)
        # Delete the PDF file from storage
        document = get_object_or_404(Plan, pk=plan_id)
        file_path = document.pdf.path
        if os.path.exists(file_path):
            os.remove(file_path)
            document.delete()
            print("Plan deleted")

        return redirect('reports:all_plans', project_id=project_id)  # Redirect to a success page

    return render(request, 'reports/all_plans.html', {'error_message': "Document could not be deleted."})


@login_required(login_url='reports:login')
def edit_invoice(request, project_id, draw_id, invoice_id):
    project = get_object_or_404(Project, pk=project_id)
    draw = get_object_or_404(Draw, pk=draw_id)
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    subs = Subcontractor.objects.order_by('name')

    context = {
        'subs': subs,
        'project': project,
        'invoice': invoice,
        'draw': draw,
        'method_choices': METHOD_OPTIONS,
        'lien_release_type_choices': LIEN_RELEASE_OPTIONS
    }

    if request.method == 'POST':
        invoice_date = request.POST.get('invoice_date')
        invoice_num = request.POST.get('invoice_num')
        division_code = request.POST.get('division_code')
        method = request.POST.get('method')
        sub_name = request.POST.get('sub')
        sub = get_object_or_404(Subcontractor, name=sub_name)
        invoice_total = request.POST.get('invoice_total')
        description = request.POST.get('description')
        lien_release_type = request.POST.get('lien_release_type')
        w9 = request.POST.get('w9')
        signed = request.POST.get('signed', False)

        if not invoice_date or not invoice_num or not division_code or not method or not sub or not invoice_total or not description or not lien_release_type or not w9:
            context.update({'error_message': "Please fill out all fields"})
            return render(request, 'reports/edit_invoice.html', context)

        invoice.invoice_date = invoice_date
        invoice.invoice_num = invoice_num
        invoice.division_code = division_code
        invoice.method = method
        invoice.sub = sub
        invoice.invoice_total = invoice_total
        invoice.description = description
        invoice.lien_release_type = lien_release_type
        invoice.w9 = w9
        invoice.signed = signed

        # Handle invoice PDF
        if 'invoice_pdf' in request.FILES:
            invoice.invoice_pdf = request.FILES['invoice_pdf']
            if not invoice.invoice_pdf.file.content_type.startswith('application/pdf'):
                context.update({'error_message': "Only PDFs are allowed for the Invoice PDF"})
                return render(request, 'reports/edit_invoice.html', context)

        # Handle lien release PDF
        if 'lien_release_pdf' in request.FILES:
            invoice.lien_release_pdf = request.FILES['lien_release_pdf']
            if not invoice.lien_release_pdf.file.content_type.startswith('application/pdf'):
                context.update({'error_message': "Only PDFs are allowed for the Lien Release PDF"})
                return render(request, 'reports/edit_invoice.html', context)

        else:
            invoice.signed = None

        # Save invoice and related objects
        project.edited_by = request.user.username
        project.date = datetime.datetime.now()
        project.save()

        draw.edited_by = request.user.username
        draw.date = datetime.datetime.now()
        draw.save()

        invoice.save()

        return redirect('reports:draw_view', project_id=project_id, draw_id=draw_id)  # Redirect to a success page

    return render(request, 'reports/edit_invoice.html', context)

@login_required(login_url='reports:login')
def draw_view(request, project_id, draw_id):
    project = get_object_or_404(Project, pk=project_id)
    draw = get_object_or_404(Draw, pk=draw_id)
    invoices = Invoice.objects.order_by('-invoice_date').filter(draw_id=draw.id)

    total_invoice_amount = invoices.aggregate(total=Sum('invoice_total'))['total']

    return render(request, 'reports/draw_view.html', {'draw': draw, 'invoices': invoices, 'total_invoice_amount':total_invoice_amount,'project': project})


@login_required(login_url='reports:login')
def contract_pdf_view(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    pdf_bytes = contract.pdf.read()
    pdf_data = base64.b64encode(pdf_bytes).decode('utf-8')
    return render(request, 'reports/contract_pdf_view.html', {'pdf_data': pdf_data, 'contract': contract})


@login_required(login_url='reports:login')
def plan_view(request, plan_id, project_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    pdf_bytes = plan.pdf.read()
    pdf_data = base64.b64encode(pdf_bytes).decode('utf-8')
    return render(request, 'reports/plan_view.html', {'pdf_data': pdf_data, 'plan': plan})



@login_required(login_url='reports:login')
def delete_invoice(request, project_id, draw_id, invoice_id):
    project = get_object_or_404(Project, pk=project_id)
    draw = get_object_or_404(Draw, pk=draw_id)
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    if request.method == 'POST':
        print("Attempting to delete invoice")
        # Delete the PDF file from storage
        if invoice.invoice_pdf:
            if os.path.exists(invoice.invoice_pdf.path):
                os.remove(invoice.invoice_pdf.path)
                invoice.invoice_pdf.delete()
        if invoice.lien_release_pdf:
            if os.path.exists(invoice.lien_release_pdf.path):
                os.remove(invoice.lien_release_pdf.path)
                invoice.lien_release_pdf.delete()

        invoice.delete()
        return redirect('reports:draw_view', project_id=project_id, draw_id=draw_id)  # Redirect to a success page

    return render(request, 'reports/draw_view.html', {'project': project, 'draw':draw, 'error_message': "Document could not be deleted."})

    project.date = datetime.datetime.now()
    draw.date = datetime.datetime.now()


@login_required(login_url='reports:login')
def purchase_orders(request, project_id, sub_id):
    project = get_object_or_404(Project, pk=project_id)
    sub = get_object_or_404(Subcontractor, pk=sub_id)
    if request.method == 'POST':
        pass

    else:
        return render(request, 'reports/purchase_orders.html', {'project': project, 'sub': sub})

@login_required(login_url='reports:login')
def new_purchase_order(request, project_id, sub_id):
    project = get_object_or_404(Project, pk=project_id)
    sub = get_object_or_404(Subcontractor, pk=sub_id)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'reports/new_purchase_order.html', {'project': project, 'sub': sub})


@login_required(login_url='reports:login')
def deductive_change_orders(request, project_id, sub_id):
    project = get_object_or_404(Project, pk=project_id)
    sub = get_object_or_404(Subcontractor, pk=sub_id)
    if request.method == 'POST':
        pass

    else:
        return render(request, 'reports/deductive_change_orders.html', {'project': project, 'sub': sub})

@login_required(login_url='reports:login')
def new_deductive_change_order(request, project_id, sub_id):
    project = get_object_or_404(Project, pk=project_id)
    sub = get_object_or_404(Subcontractor, pk=sub_id)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'reports/new_deductive_change_order.html', {'project':project, 'sub': sub})

@login_required(login_url='reports:login')
def change_orders(request, project_id, sub_id):
    project = get_object_or_404(Project, pk=project_id)
    sub = get_object_or_404(Subcontractor, pk=sub_id)
    cos = ChangeOrder.objects.order_by('-date')

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('scope'):
                # Handle scope field
                scope_index = key.replace('scope', '')
                scope_value = value
                # Process the scope value

                # Get corresponding qty, unitprice, and totalprice values
                qty_key = f'qty{scope_index}'
                unitprice_key = f'unitprice{scope_index}'
                totalprice_key = f'totalprice{scope_index}'

                qty_value = request.POST.get(qty_key)
                unitprice_value = request.POST.get(unitprice_key)
                totalprice_value = request.POST.get(totalprice_key)

                if scope_value == "" or float(qty_value) <= 0 or float(unitprice_value) <= 0:
                    return render(request, 'reports/new_change_order.html', {'project': project, 'sub': sub, 'error_message': "All fields need to be filled."})

                try:
                    qty_value = int(qty_value)
                    unitprice_value = float(unitprice_value)
                except ValueError:
                    return render(request, 'reports/new_change_order.html', {'project': project, 'sub': sub, 'error_message': "'Qty' and 'Unit Price' fields must be numbers."})

                co = ChangeOrder()
                co.order_number = f"{project.name} CO {datetime.datetime.now().year % 100}{len(ChangeOrder.objects.all())+1}{datetime.datetime.now().month}"
                co.date = datetime.datetime.now()
                co.sub_id = sub
                co.project_id = project

                co.save()
                #create PDF HERE

        return redirect('reports:change_orders', project_id=project_id, sub_id=sub_id)
    else:
        return render(request, 'reports/change_orders.html', {'project': project, 'sub': sub, 'cos': cos})


@login_required(login_url='reports:login')
def new_change_order(request, project_id, sub_id):
    project = get_object_or_404(Project, pk=project_id)
    sub = get_object_or_404(Subcontractor, pk=sub_id)

    return render(request, 'reports/new_change_order.html', {'project': project, 'sub': sub})


@login_required(login_url='reports:login')
def delete_change_order(request, co_id):
    co = get_object_or_404(ChangeOrder, pk=co_id)

    file_path = co.pdf.path
    if os.path.exists(file_path):
        os.remove(file_path)
        co.delete()

    return redirect('reports:change_orders', project_id=co.project_id, sub_id=co.sub_id)


@login_required(login_url='reports:login')
def contract_view(request, project_id, sub_id):
    project = get_object_or_404(Project, pk=project_id)
    sub = get_object_or_404(Subcontractor, pk=sub_id)
    contracts = Contract.objects.order_by("-date").filter(sub_id=sub)
    print(contracts)
    context = {
        'project': project,
        'sub': sub,
        'contracts': contracts
    }

    if request.method == 'POST':
        form_type = request.POST.get('form-type')
        if form_type == 'contract':
            contract = Contract()
            contract.date = datetime.datetime.now()
            contract.total = request.POST.get('total')
            contract.sub_id = sub
            contract.project_id = project
            contract.pdf = request.POST.get('contract_pdf')

            try:
                contract.total = float(contract.total)
                if contract.total <= 0:
                    context.update({'error_message': "Total must be a positive number and not 0"})
                    return render(request, 'reports/contract_view.html', context)
            except:
                context.update({'error_message': "Total must be a number"})
                return render(request, 'reports/contract_view.html', context)

            if not contract.pdf.file.content_type.startswith('application/pdf'):
                context.update({'error_message': "Only PDFs are allowed for the PDF"})
                return render(request, 'reports/contract_view.html', context)

    return render(request, 'reports/contract_view.html', context)


@login_required(login_url='reports:login')
def invoice_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    pdf_bytes = invoice.invoice_pdf.read()
    pdf_data = base64.b64encode(pdf_bytes).decode('utf-8')
    return render(request, 'reports/invoice_view.html', {'pdf_data': pdf_data, 'invoice': invoice})



