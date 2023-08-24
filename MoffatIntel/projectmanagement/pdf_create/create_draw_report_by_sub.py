import os
import tempfile

from django.conf import settings
from django.core.files.base import ContentFile
from datetime import datetime
from fpdf import FPDF
from ..models import GeneratedReport


def create_draw_report_by_sub(project, draws, sub, vendor, checks, invoices, exhibits, groups):
    print(project, draws, sub, vendor, checks, invoices, exhibits, groups)
    if not project or not draws or not (sub or vendor) or not checks or not invoices or not exhibits or not groups:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=20)

        # Center text on the page
        text = "NOT ENOUGH DATA TO GENERATE REPORT"
        text_width = pdf.get_string_width(text)
        page_width = pdf.w - 2 * pdf.l_margin
        x_position = (page_width - text_width) / 2
        pdf.set_x(x_position)
        pdf.cell(text_width, 10, text, ln=True)

        # Output PDF
        file_name = 'Report Failure.pdf'

        if os.path.exists(file_name + ".pdf"):
            counter = 1
            while os.path.exists(file_name + "(" + str(counter) + ")" + ".pdf"):
                counter += 1
            file_name += "(" + str(counter) + ")"

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file_path = temp_file.name
        pdf.output(temp_file_path)

        with open(temp_file_path, 'rb') as file:
            file_content = file.read()

        file_data = ContentFile(file_content)

        report = GeneratedReport()
        report.name = file_name
        report.date = datetime.now()
        report.pdf.save(file_name, file_data)

        report.save()
        temp_file.close()

        os.remove(temp_file_path)
        return report

    if sub:
        file_name = project.name + " " + sub.name + " " + str(datetime.now().strftime("%B-%d-%Y"))

    elif vendor:
        file_name = project.name + " " + vendor.name + " " + str(datetime.now().strftime("%B-%d-%Y"))
        sub = vendor

    if os.path.exists(file_name + ".pdf"):
        counter = 1
        while os.path.exists(file_name + "(" + str(counter) + ")" + ".pdf"):
            counter += 1
        file_name += "(" + str(counter) + ")"

    file_name += ".pdf"

    pdf = FPDF()

    pdf.set_title(file_name[:len(file_name) - 4])
    pdf.set_author("Moffat Construction")
    pdf.set_font("Arial", size=10)

    # Set margins (3/4 inch margins)
    margin = 20
    pdf.set_auto_page_break(auto=True, margin=margin)

    # Add a new page
    pdf.add_page()

    # Add image at the top center
    pdf.image(os.path.join(settings.BASE_DIR, 'projectmanagement\static\\projectmanagement\images\logo.png'),
              x=(pdf.w / 2) - 40, y=10, w=80, h=18)
    pdf.ln(23)

    pdf.set_font("Arial", style="B", size=12)
    pdf.set_line_width(.6)
    pdf.cell(pdf.w - 20, 10, f"{project.name.upper()} - BUILDING COST SUMMARY FOR {sub.name.upper()} - {str(datetime.now().strftime('%B-%d-%Y'))}", 1, 0, align="C")
    pdf.ln(15)

    pdf.set_font("Arial", size=10)

    pdf.set_fill_color(217, 225, 242)
    pdf.cell(pdf.w - 20, 5, "Payment Control", 1, 0, "C", True)
    pdf.set_fill_color(256)
    pdf.ln(10)

    pdf.set_line_width(.25)
    pdf.set_xy(10, pdf.get_y())
    pdf.cell((pdf.w - 20) * .14, 5, 'Draw #', 1, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Check #', 1, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Check Amt', 1, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Date Paid', 1, 0, 'C', True)
    pdf.cell(.1, 5, '', 1, 0, 'C', True)

    pdf.cell((pdf.w - 20) * .14, 5, 'Retention', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, '% Drawn', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Payable', 0, 0, 'C', True)

    for group in groups:
        pdf.ln(10)
        pdf.set_fill_color(217, 225, 242)
        pdf.cell(pdf.w - 20, 5, f"{group.name.upper()}", 1, 0, "C", True)
        pdf.set_fill_color(256)
        pdf.ln(15)

        cur_invoice = None
        cur_check = None
        paid_total = 0.00
        bldg_contract = 0.00
        bldg_pct_paid = 0.00

        for exhibit in exhibits:
            pass

        for invoice in invoices:
            if invoice.group_id == group.id:
                print(invoice)
                cur_invoice = invoice

        if cur_invoice:
            for check in checks:
                if check.invoice_id == cur_invoice.id:
                    cur_check = check
                    paid_total += cur_check.check_total

            for draw in draws:
                if cur_invoice.draw_id == draw.id:
                    pdf.cell((pdf.w - 20) * .14, 5, draw.num, 1, 0, 'C', True)
                    pdf.cell((pdf.w - 20) * .14, 5, cur_check.check_num, 1, 0, 'C', True)
                    pdf.cell((pdf.w - 20) * .14, 5, cur_check.check_total, 1, 0, 'R', True)
                    pdf.cell((pdf.w - 20) * .14, 5, str(cur_check.check_date.strftime("%m/%d/$Y")), 1, 0, 'C', True)
                    if pdf.get_y() + 65 > pdf.page_break_trigger:
                        pdf.add_page()
                        pdf.ln(15)

        pdf.ln(10)
        pdf.set_xy(10, pdf.get_y())
        pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, 'Bldg Contract', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, 'Bldg Paid', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, 'Bldg Retention', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, 'Bldg % Paid', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, 'Bldg Payable', 0, 0, 'C', True)

        pdf.ln(5)
        pdf.set_xy(10, pdf.get_y())
        pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, f'${paid_total:.2f}', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
        pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)

        if pdf.get_y() + 65 > pdf.page_break_trigger:
            pdf.add_page()
            pdf.ln(15)

    pdf.set_xy(10, pdf.get_y())
    pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Contract Value', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Total Paid', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Total Retention', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Total % Paid', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, 'Total Payable', 0, 0, 'C', True)
    pdf.ln(5)
    pdf.set_fill_color(217, 225, 242)
    pdf.set_xy(10, pdf.get_y())
    pdf.cell((pdf.w - 20) * .14, 5, 'Total:', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)
    pdf.cell((pdf.w - 20) * .14, 5, '', 0, 0, 'C', True)

    # Generate the full file path
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file_path = temp_file.name
    pdf.output(temp_file_path)
    with open(temp_file_path, 'rb') as file:
        file_content = file.read()

    file_data = ContentFile(file_content)

    report = GeneratedReport()
    report.name = file_name
    report.date = datetime.now()
    report.pdf.save(file_name, file_data)

    report.save()
    temp_file.close()

    os.remove(temp_file_path)
    return report