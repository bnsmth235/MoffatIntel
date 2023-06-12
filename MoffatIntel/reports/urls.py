from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('all/', views.all, name='all'),
    path('new_proj/', views.new_proj, name='new_proj'),
    path('input_data/', views.input_data, name='input_data'),
    path('todo/', views.todo, name='todo'),
    path('new_contract/', views.new_contract, name='new_contract'),

    path('contract_pdf_view/<int:contract_id>/', views.contract_pdf_view, name='contract_pdf_view'),
    path('exhibit_pdf_view/<int:exhibit_id>/', views.exhibit_pdf_view, name='exhibit_pdf_view'),
    path('swo_pdf_view/<int:swo_id>/', views.swo_pdf_view, name='swo_pdf_view'),
    path('co_pdf_view/<int:co_id>/', views.co_pdf_view, name='co_pdf_view'),
    path('po_pdf_view/<int:po_id>/', views.po_pdf_view, name='po_pdf_view'),
    path('dco_pdf_view/<int:dco_id>/', views.dco_pdf_view, name='dco_pdf_view'),
    path('prop_pdf_view/<int:prop_id>/', views.prop_pdf_view, name='prop_pdf_view'),

    path('delete_exhibit/<int:exhibit_id>/', views.delete_exhibit, name='delete_exhibit'),
    path('delete_contract/<int:contract_id>/', views.delete_contract, name='delete_contract'),
    path('delete_swo/<int:swo_id>/', views.delete_swo, name='delete_swo'),
    path('delete_prop/<int:prop_id>/', views.delete_prop, name='delete_prop'),
    path('delete_sub/<int:sub_id>/', views.delete_sub, name='delete_sub'),
    path('delete_proj/<int:project_id>/', views.delete_proj, name='delete_proj'),
    path('delete_vendor/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),
    path('delete_change_order/<int:co_id>/', views.delete_change_order, name='delete_change_order'),
    path('delete_invoice/<int:project_id>/<int:draw_id>/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('delete_plan/<int:project_id>', views.delete_plan, name='delete_plan'),
    path('delete_deductive_change_order/<int:dco_id>/', views.delete_deductive_change_order, name='delete_deductive_change_order'),
    path('delete_purchase_order/<int:po_id>/', views.delete_purchase_order, name='delete_purchase_order'),
    path('delete_draw/<int:project_id>/', views.delete_draw, name='delete_draw'),

    path('all_subs/', views.all_subs, name='all_subs'),
    path('all_vendors/', views.all_vendors, name='all_vendors'),
    path('all_draws/<int:project_id>/', views.all_draws, name='all_draws'),
    path('all_plans/<int:project_id>', views.all_plans, name='all_plans'),

    path('edit_sub/<int:sub_id>/',views.edit_sub, name='edit_sub'),
    path('edit_invoice/<int:project_id>/<int:draw_id>/<int:invoice_id>/', views.edit_invoice, name='edit_invoice'),
    path('edit_vendor/<int:vendor_id>/',views.edit_vendor, name='edit_vendor'),
    path('edit_proj/<int:project_id>/', views.edit_proj, name='edit_proj'),

    path('new_draw/<int:project_id>', views.new_draw, name='new_draw'),
    path('new_invoice/<int:project_id>/<int:draw_id>/', views.new_invoice, name='new_invoice'),
    path('new_change_order/<int:project_id>/<int:sub_id>/', views.new_change_order, name='new_change_order'),
    path('new_change_order/', views.new_change_order, name='new_change_order'),
    path('new_deductive_change_order', views.new_deductive_change_order, name='new_deductive_change_order'),
    path('new_purchase_order/<int:project_id>/', views.new_purchase_order, name='new_purchase_order'),
    path('new_purchase_order/', views.new_purchase_order, name='new_purchase_order'),
    path('new_exhibit/<int:project_id>/<int:sub_id>/', views.new_exhibit, name='new_exhibit'),

    path('contract_view/<int:project_id>/<int:sub_id>', views.contract_view, name='contract_view'),
    path('draw_view/<int:project_id>/<int:draw_id>/', views.draw_view, name='draw_view'),
    path('plan_view/<int:project_id>/<int:plan_id>/', views.plan_view, name='plan_view'),
    path('invoice_view/<int:invoice_id>/', views.invoice_view, name='invoice_view'),
    path('project_view/<int:project_id>/', views.project_view, name='project_view'),
    path('sub_select/<int:project_id>/', views.sub_select, name='sub_select'),
    path('add_signature/<int:invoice_id>/', views.add_signature, name='add_signature'),
    path('change_orders/<int:project_id>/<int:sub_id>/', views.change_orders, name='change_orders'),
    path('deductive_change_orders/<int:project_id>/<int:sub_id>/', views.deductive_change_orders, name='deductive_change_orders'),
    path('purchase_orders/<int:project_id>/', views.purchase_orders, name='purchase_orders'),
    path('upload_plan/<int:project_id>/', views.upload_plan, name='upload_plan'),

    path('log_out/', views.log_out, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]
app_name = "reports"
