from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^supplier/add_supplier/$', views.add_supplier, name='add_supplier'),
    url(r'^(?P<supplier_id>[0-9]+)/update_supplier/$', views.update_supplier, name='update_supplier'),
    url(r'^supplier/manage_supplier/$',views.manage_supplier, name='manage_supplier'),
    url(r'^delete_supplier/(?P<supplier_id>[0-9]+)/$', views.delete_supplier, name='delete_supplier'),
    url(r'^product/category/$', views.category, name='category'),
    url(r'^product/category1/$', views.category1, name='category1'),
    url(r'^delete_category/(?P<category_id>[0-9]+)/$', views.delete_category, name='delete_category'),
    url(r'^product/subcategory/$', views.subcategory, name='subcategory'),
    url(r'^product/subcategory1/$', views.subcategory1, name='subcategory1'),
    url(r'^delete_subcategory/(?P<subcategory_id>[0-9]+)/$', views.delete_subcategory, name='delete_subcategory'),
    url(r'^update_product/(?P<product_id>[0-9]+)/$', views.update_product, name='update_product'),
    url(r'^product/add_product/$', views.add_product, name='add_product'),
    url(r'^product/add_product1/$', views.add_product1, name='add_product1'),
    url(r'^get_product/$', views.get_product, name='get_product'),
    url(r'^product/manage_product/$', views.manage_product, name = 'manage_product'),
    url(r'^product/manage_product/view_product/(?P<product_id>[0-9]+)/$', views.view_product, name = 'view_product'),
    url(r'^delete_product/(?P<product_id>[0-9]+)/$', views.delete_product, name='delete_product'),
    url(r'^customer/add_customer1/$', views.add_customer1, name='add_customer1'),
    url(r'^customer/add_customer/$', views.add_customer, name='add_customer'),
    url(r'^customer/manage_customer/$', views.manage_customer, name = 'manage_customer'),
    url(r'^customer/delete_customer/(?P<customer_id>[0-9]+)/$', views.delete_customer, name='delete_customer'),
    url(r'^customer/update_customer/(?P<customer_id>[0-9]+)/$', views.update_customer, name='update_customer'),
    #url(r'^add_employee/$', views.add_employee, name='add_employee'),
    url(r'^business_profile/$',views.business_profile, name='business_profile'),
    url(r'^settings/localization/$',views.localization, name='localization'),

    url(r'^get_purchase/$', views.get_purchase, name='get_purchase'),
    url(r'^purchase/new_purchase/$', views.new_purchase, name='new_purchase'),
    url(r'^purchase/new_purchase/purchase/(?P<purchase_id>[0-9]+)/$', views.new_purchase_purchase, name='new_purchase_purchase'),

    url(r'^purchase/new_purchase/invoice/(?P<purchase_id>[0-9]+)/$', views.purchase_invoice, name='purchase_invoice'),

    url(r'^purchase/manage_purchase/invoice/(?P<purchase_id>[0-9]+)/$', views.invoice, name='invoice'),
    url(r'^purchase/manage_purchase/$', views.manage_purchase, name='manage_purchase'),
    url(r'^report/stock_report/$',views.stock_report, name='stock_report'),

    url(r'^order/new_order/$',views.new_order, name='new_order'),
    url(r'^order/new_order/order/(?P<order_id>[0-9]+)/$',views.new_order_order, name='new_order_order'),
    url(r'^order/new_order/checkout/(?P<order_id>[0-9]+)/$',views.checkout, name='checkout'),

    url(r'^get_discount/$', views.get_discount, name='get_discount'),
    url(r'^order/new_order/invoice/(?P<order_id>[0-9]+)/$', views.order_invoice, name='order_invoice'),
    url(r'^order/manage_order/$',views.manage_order, name='manage_order'),
    url(r'^order/manage_order/invoice/(?P<order_id>[0-9]+)/$',views.ordinvoice, name='ordinvoice'),
    url(r'^report/sales_report/$',views.sales_report, name='sales_report'),
    url(r'^report/sales_report1/$',views.sales_report1, name='sales_report1'),
    url(r'^report/sales_summary_report/$',views.sales_summary_report, name='sales_summary_report'),
    url(r'^report/sales_summary_report1/$',views.sales_summary_report1, name='sales_summary_report1'),
    url(r'^report/purchase_report/$',views.purchase_report, name='purchase_report'),
    url(r'^report/purchase_report1/$',views.purchase_report1, name='purchase_report1'),
    url(r'^notification/$',views.notification, name='notification'),
    url(r'^cancelled_order/$',views.cancelled_order, name='cancelled_order'),
    url(r'^forgot_pasword/$',views.forgot_password, name='forgot_password'),
    url(r'^submit/$',views.submit, name='submit'),


]

