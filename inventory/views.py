# -*- coding: utf-8 -*-
import itertools
import json
import datetime
import operator
import calendar

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterForm, AddSupplierForm, CategoryForm, SubCategoryForm, AddProductForm, AddCustomerForm, \
    BusinessProfileForm, LocalizationForm, IDForm, SalesForm
from .models import Supplier, Product, Category, SubCategory, Customer, BusinessProfile, Purchase, PInvoice, Dashboard, \
    Order, OInvoice, Localization


def start(request):
    return render(request, 'inventory/start.html')


def about_us(request):
    return render(request, 'inventory/about_us.html')


def contact(request):
    return render(request, 'inventory/contact.html')


def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        users = User.objects.all()
        for user in users:
            if user.username == username:
                return render(request,'inventory/login.html')
    return render(request, 'inventory/forget_password.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                orders = Order.objects.filter(user=request.user, date__year=datetime.date.today().year)
                orderss = Order.objects.filter(user=request.user, date__month=datetime.date.today().month)
                dic = {}
                for order in orderss:
                    if order.status == 1:
                        ois = OInvoice.objects.filter(order=order.id)
                        for pi in ois:
                            product = Product.objects.get(pk=pi.product.id)
                            if product in dic.keys():
                                dic[product] = dic[product] + pi.quantity
                            else:
                                dic[product] = pi.quantity
                sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
                lis = []
                if len(sorted_x) > 5:
                    for i in range(5):
                        lis.append(sorted_x[i][0])
                else:
                    for i in range(len(sorted_x)):
                        lis.append(sorted_x[i][0])

                dic = {}
                for order in orders:
                    if order.status == 1:
                        ois = OInvoice.objects.filter(order=order.id)
                        for pi in ois:
                            product = Product.objects.get(pk=pi.product.id)
                            if product in dic.keys():
                                dic[product] = dic[product] + pi.quantity
                            else:
                                dic[product] = pi.quantity
                sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
                li = []
                if len(sorted_x) > 5:
                    for i in range(5):
                        li.append(sorted_x[i][0])
                else:
                    for i in range(len(sorted_x)):
                        li.append(sorted_x[i][0])
                orders = Order.objects.filter(user=request.user).order_by('-date')
                print(orders)
                lit = []
                i = 0
                for order in orders:
                    if i == 5:
                        break
                    lit.append(order)
                    i += 1

                month = calendar.month_name[datetime.date.today().month]
                return render(request, 'inventory/dashboard.html', {
                    'date': datetime.date.today(),
                    'products': li,
                    'productss': lis,
                    'orders': lit,
                    'month': month,
                })

            else:
                return render(request, 'inventory/login.html', {'error_message': 'Your account has been disabled', })
        else:
            return render(request, 'inventory/login.html', {'status': 0})
    return render(request, 'inventory/login.html', {'status': 1})


def logout_user(request):
    logout(request)
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'inventory/login.html', context)

    '''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                customer = Customer.objects.filter(user=request.user)
                supplier = Supplier.objects.filter(user=request.user)
                return render(request, 'inventory/start.html', {
                    'customer': customer,
                    'supplier': supplier,
                })
            else:
                return render(request, 'inventory/login.html', {
                    'error_message': 'Your account has been disabled'
                })
        else:
            return render(request, 'inventory/login.html', {'error_message': 'Invalid login'})
    return render(request,'inventory/login.html')
'''


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        '''user1= User1()
        user1.username = form.cleaned_data.get('username')
        user1.password = form.cleaned_data.get('password')
        user1.email = form.cleaned_data.get('email')
        user1.first_name = form.cleaned_data.get('first_name')
        user1.last_name = form.cleaned_data.get('last_name')
        user1.password1 = form.cleaned_data.get('password1')
        user1.phone_number = form.cleaned_data.get('phone_number')
        if not user1.password1 == user1.password:
            return render(request, 'inventory/register.html', {
                'form': form,
                'error_message': 'Password didn\'t match',
            })
        user1.save()'''
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                orders = Order.objects.filter(user=request.user, date__year=datetime.date.today().year)
                orderss = Order.objects.filter(user=request.user, date__month=datetime.date.today().month)
                dic = {}
                for order in orderss:
                    if order.status == 1:
                        ois = OInvoice.objects.filter(order=order.id)
                        for pi in ois:
                            product = Product.objects.get(pk=pi.product.id)
                            if product in dic.keys():
                                dic[product] = dic[product] + pi.quantity
                            else:
                                dic[product] = pi.quantity
                sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
                lis = []
                if len(sorted_x) > 5:
                    for i in range(5):
                        lis.append(sorted_x[i][0])
                else:
                    for i in range(len(sorted_x)):
                        lis.append(sorted_x[i][0])

                dic = {}
                for order in orders:
                    if order.status == 1:
                        ois = OInvoice.objects.filter(order=order.id)
                        for pi in ois:
                            product = Product.objects.get(pk=pi.product.id)
                            if product in dic.keys():
                                dic[product] = dic[product] + pi.quantity
                            else:
                                dic[product] = pi.quantity
                sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
                li = []
                if len(sorted_x) > 5:
                    for i in range(5):
                        li.append(sorted_x[i][0])
                else:
                    for i in range(len(sorted_x)):
                        li.append(sorted_x[i][0])
                orders = Order.objects.filter(user=request.user).order_by('-date')
                print(orders)
                lit = []
                i = 0
                for order in orders:
                    if i == 5:
                        break
                    lit.append(order)
                    i += 1

                month = calendar.month_name[datetime.date.today().month]
                return render(request, 'inventory/dashboard.html', {
                    'date': datetime.date.today(),
                    'products': li,
                    'productss': lis,
                    'orders': lit,
                    'month': month,
                })

    return render(request,'inventory/register.html', {
        'form': form,
    })

    '''
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                supplier = Supplier.objects.filter(user=request.user)
                customer = Customer.objects.filter(user=request.user)
                return render(request, 'inventory/start.html', {
                    'supplier': supplier,
                    'customer': customer
                })
    context = {
        "form": form,
    }
    return render(request, 'inventory/register.html', context)
'''


def dashboard(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        orders = Order.objects.filter(user=request.user, date__year=datetime.date.today().year)
        orderss = Order.objects.filter(user=request.user,date__month=datetime.date.today().month)
        dic = {}
        for order in orderss:
            if order.status == 1:
                ois = OInvoice.objects.filter(order=order.id)
                for pi in ois:
                    product = Product.objects.get(pk=pi.product.id)
                    if product in dic.keys():
                        dic[product] = dic[product] + pi.quantity
                    else:
                        dic[product] = pi.quantity
        sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
        lis = []
        if len(sorted_x) > 5:
            for i in range(5):
                lis.append(sorted_x[i][0])
        else:
            for i in range(len(sorted_x)):
                lis.append(sorted_x[i][0])

        dic = {}
        for order in orders:
            if order.status == 1:
                ois = OInvoice.objects.filter(order=order.id)
                for pi in ois:
                    product = Product.objects.get(pk=pi.product.id)
                    if product in dic.keys():
                        dic[product] = dic[product] + pi.quantity
                    else:
                        dic[product] = pi.quantity
        sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
        li = []
        if len(sorted_x) > 5:
            for i in range(5):
                li.append(sorted_x[i][0])
        else:
            for i in range(len(sorted_x)):
                li.append(sorted_x[i][0])
        orders = Order.objects.filter(user=request.user).order_by('-date')
        print(orders)
        lit=[]
        i=0
        for order in orders:
            if i==5:
                break
            lit.append(order)
            i+=1
        month = calendar.month_name[datetime.date.today().month]
        return render(request, 'inventory/dashboard.html', {
            'date': datetime.date.today(),
            'products': li,
            'productss': lis,
            'orders': lit,
            'month': month,
        })


def add_supplier(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = AddSupplierForm(request.POST or None)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.company_name = form.cleaned_data.get('company_name')
            supplier.supplier_name = form.cleaned_data.get('supplier_name')
            supplier.email = form.cleaned_data.get('email')
            supplier.phone_number = form.cleaned_data.get('phone_number')
            supplier.address = form.cleaned_data.get('address')
            supplier.user = request.user
            supplier.save()
            product = Product.objects.filter(user=request.user)
            category1 = Category.objects.filter(user=request.user)
            suppliers = Supplier.objects.filter(user=request.user)
            return render(request, 'inventory/manage_supplier.html', {
                'product': product,
                'category': category1,
                'suppliers': suppliers,
            })
        return render(request, 'inventory/add_supplier.html', {
            'form': form,
        })


def manage_supplier(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        suppliers = Supplier.objects.filter(user=request.user)
        return render(request, 'inventory/manage_supplier.html',{
            'suppliers': suppliers,
        })

'''
class UpdateSupplier(UpdateView):
    model = Supplier
    fields = ['company_name', 'supplier_name', 'email', 'phone_number', 'address']'''


def update_supplier(request, supplier_id):
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
    except Supplier.DoesNotExist:
        supplier = None
    if supplier is None:
        return render(request,'inventory/manage_supplier.html')
    form = AddSupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        suppliers = Supplier.objects.filter(user=request.user)
        return render(request, 'inventory/manage_supplier.html', {
            'suppliers': suppliers,
        })
    return render(request, 'inventory/add_supplier.html', {'form': form})


def update_product(request, product_id):
    suppliers = Supplier.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None
    if product is None:
        return render(request,'inventory/manage_product.html')
    form = AddProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save(commit=False)
        products = Product.objects.filter(user=request.user)
        q = 0
        p = 0.0
        total = 0.0
        for product in products:
            q = product.quantity
            p = product.cost_price
            total += float(q) * float(p)
        return render(request, 'inventory/manage_product.html', {
            'stock': total,
        })
    return render(request, 'inventory/add_product.html', {
        'form': form,
        'categories': categories,
        'suppliers': suppliers
    })


def update_customer(request, customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        customer = None
    if customer is None:
        return render(request,'inventory/manage_customer.html')
    form = AddCustomerForm(request.POST or None, instance=customer)
    print("-------------------------------" , form)
    if form.is_valid():
        form.save()
        customer1 = Customer.objects.filter(user=request.user)
        return render(request, 'inventory/manage_customer.html', {
            'customers': customer1,
        })
    return render(request, 'inventory/add_customer.html', {'form': form})



def delete_supplier(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    supplier.delete()
    suppliers = Supplier.objects.filter(user=request.user)
    return render(request, 'inventory/manage_supplier.html', {
        'suppliers': suppliers,
    })


def category1(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        category2 = Category.objects.filter(user=request.user)
        return render(request, 'inventory/category.html', {
            'category': category2,
        })


def category(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            category1 = form.save(commit=False)
            category1.product_category = form.cleaned_data.get('product_category')
            category1.user = request.user
            category1.save()
            category2 = Category.objects.filter(user=request.user)
            return render(request, 'inventory/category.html', {
                'category': category2,
            })
        return render(request, 'inventory/category.html', {
            'form': form,
        })


def subcategory1(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        iterator = itertools.count()
        iterator.next
        categories = Category.objects.filter(user=request.user)
        return render(request, 'inventory/subcategory.html', {
            'categories': categories,
            'iterator': iterator,
        })


def subcategory(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        categories = Category.objects.filter(user=request.user)
        form = SubCategoryForm(request.POST or None)
        if form.is_valid():
            categor = form.cleaned_data.get('product_category')
            category = Category.objects.get(product_category=categor, user=request.user)
            category_sub = category.subcategory_set.all()
            for c in category_sub:
                if c.product_subcategory == form.cleaned_data.get('product_subcategory'):
                    return render(request, 'inventory/subcategory.html', {
                        'categories': categories,
                        'error_message': 'We already have that category',
                    })
            subcategory = form.save(commit=False)
            subcategory.product_category= category
            subcategory.product_subcategory = form.cleaned_data.get('product_subcategory')
            subcategory.user = request.user
            subcategory.save()
            iterator = itertools.count()
            return render(request, 'inventory/subcategory.html', {
                'categories': categories,
                'iterator': iterator,
            })
        return render(request, 'inventory/subcategory.html', {
            'categories': categories,
            'form': form
        })


def add_product(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = AddProductForm(request.POST or None)
        suppliers = Supplier.objects.filter(user=request.user)
        categories = Category.objects.filter(user=request.user)
        subcategories = SubCategory.objects.all()
        if form.is_valid():
            print("------------------",form.cleaned_data,request.FILES['product_image'])
            product = form.save(commit=False)
            product.user = request.user
            product.product_code = form.cleaned_data.get('product_code')
            product.product_name = form.cleaned_data.get('product_name')
            product.supplier = form.cleaned_data.get('supplier')
            product.product_category = form.cleaned_data.get('product_category')
           # print("-------------------",product.product_category)
            #subcategory = form.cleaned_data.get('product_subcategory')
            #sub1 = SubCategory.objects.get(product_subcategory= subcategory)
            product.product_subcategory = form.cleaned_data.get('product_subcategory')
            #product.tax = form.cleaned_data.get('tax')
            product.product_image = request.FILES['product_image']
            product.cost_price = form.cleaned_data.get('cost_price')
            product.selling_price = form.cleaned_data.get('selling_price')
            product.notify_quantity = form.cleaned_data.get('notify_quantity')
            product.s_date = form.cleaned_data.get('s_date')
            product.e_date = form.cleaned_data.get('e_date')
            product.price = form.cleaned_data.get('price')
            product.save()
            product1 = Product.objects.filter(user = request.user)
            return render(request, 'inventory/manage_product.html', {
                'products': product1,
            })
        #print("+++++++++++++++++++++++++++++++")
        return render(request,'inventory/add_product.html', {
            'suppliers': suppliers,
            'categories': categories,
            'form': form,
        })


def add_product1(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        suppliers = Supplier.objects.filter(user=request.user)
        categories = Category.objects.filter(user=request.user)
        #subcategories = SubCategory.objects.all()
        return render(request, 'inventory/add_product.html', {
            'suppliers': suppliers,
            'categories': categories,
        })


def manage_product(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        products = Product.objects.filter(user=request.user)
        return render(request, 'inventory/manage_product.html',{
            'products': products,
        })


def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    product2 = Product.objects.filter(user=request.user)
    return render(request, 'inventory/manage_product.html', {
        'products': product2,
    })


def add_customer(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = AddCustomerForm(request.POST or None)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.name = form.cleaned_data.get('name')
            customer.email = form.cleaned_data.get('email')
            customer.phone_number = form.cleaned_data.get('phone_number')
            customer.discount = form.cleaned_data.get('discount')
            customer.address = form.cleaned_data.get('address')
            customer.save()
            customer1 = Customer.objects.filter(user= request.user)
            return render(request, 'inventory/manage_customer.html', {
                'customers': customer1,
            })
        return render(request,'inventory/add_customer.html', {
            'form': form,
        })


def add_customer1(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        customer = Customer.objects.filter(user=request.user).aggregate(Max('id'))
        value1 = customer.get('id__max')
        if value1 is None:
            value = 0
        else:
            value = value1
        return render(request,'inventory/add_customer.html', {
            'customer': value+1,
        })


def manage_customer(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        customers = Customer.objects.filter(user=request.user)
        return render(request, 'inventory/manage_customer.html',{
            'customers': customers,
        })


def delete_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    customer.delete()
    customers = Customer.objects.filter(user=request.user)
    return render(request, 'inventory/manage_customer.html', {
        'customers': customers,
    })


def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()
    category2 = Category.objects.filter(user=request.user)
    return render(request, 'inventory/category.html', {
        'category': category2,
    })


def delete_subcategory(request, subcategory_id):
    subcategory = SubCategory.objects.get(pk = subcategory_id)
    subcategory.delete()
    subcategory2 = SubCategory.objects.filter(user=request.user)
    iterator = itertools.count()
    iterator.next
    categories = Category.objects.filter(user=request.user)
    return render(request, 'inventory/subcategory.html', {
        'categories': categories,
        'iterator': iterator,
    })


@csrf_exempt
def get_product(request):
    sclist = []
    response = {'msg': 'Yes', 'status': '1'}
    json_request = json.loads(request.body)
    category = json_request.get('category', 'All')
    # status = json_request.get('status', 'Available')
    # condition = json_request.get('condition', 'Good')
    # category1 = Category.objects.filter(user= request.user, product_category=category)
    #print("++++++++++++++------------+++++++++++",category)
    data = SubCategory.objects.filter(product_category=category)
    #print("---------",data)
    for d in data:
        dc = {"subcategory": d.product_subcategory, "id":d.id}
        sclist.append(dc)
    #print("===============0",sclist)
    response.update({'list': sclist})
    return JsonResponse(response)


@csrf_exempt
def get_purchase(request):
    sclist = []
    response = {'msg': 'Yes', 'status': '1'}
    json_request = json.loads(request.body)
    supplier = json_request.get('supplier', 'All')
    data = Product.objects.filter(supplier= supplier)
    for d in data:
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=",d.id,)
        dc = {"name": d.product_name, "id": d.id, "code": d.product_code, "quantity": d.quantity}
        sclist.append(dc)
    response.update({'list': sclist})
    return JsonResponse(response)


def business_profile(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = BusinessProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.c_logo = form.cleaned_data.get('c_logo')
            profile.c_name = form.cleaned_data.get('c_name')
            profile.c_email = form.cleaned_data.get('c_email')
            profile.c_address = form.cleaned_data.get('c_address')
            profile.c_phone = form.cleaned_data.get('c_phone')
            profile1 = get_object_or_404(BusinessProfile, pk=1)
            profile1.c_name = profile.c_name
            profile1.c_email = profile.c_email
            profile1.c_phone = profile.c_phone
            profile1.c_address = profile.c_address
            profile1.c_logo = profile.c_logo
            profile1.save()
            orders = Order.objects.filter(user=request.user, date__year=datetime.date.today().year)
            orderss = Order.objects.filter(user=request.user, date__month=datetime.date.today().month)
            dic = {}
            for order in orderss:
                if order.status == 1:
                    ois = OInvoice.objects.filter(order=order.id)
                    for pi in ois:
                        product = Product.objects.get(pk=pi.product.id)
                        if product in dic.keys():
                            dic[product] = dic[product] + pi.quantity
                        else:
                            dic[product] = pi.quantity
            sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
            lis = []
            if len(sorted_x) > 5:
                for i in range(5):
                    lis.append(sorted_x[i][0])
            else:
                for i in range(len(sorted_x)):
                    lis.append(sorted_x[i][0])

            dic = {}
            for order in orders:
                if order.status == 1:
                    ois = OInvoice.objects.filter(order=order.id)
                    for pi in ois:
                        product = Product.objects.get(pk=pi.product.id)
                        if product in dic.keys():
                            dic[product] = dic[product] + pi.quantity
                        else:
                            dic[product] = pi.quantity
            sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
            li = []
            if len(sorted_x) > 5:
                for i in range(5):
                    li.append(sorted_x[i][0])
            else:
                for i in range(len(sorted_x)):
                    li.append(sorted_x[i][0])
            orders = Order.objects.filter(user=request.user).order_by('-date')
            print(orders)
            lit = []
            i = 0
            for order in orders:
                if i == 5:
                    break
                lit.append(order)
                i += 1

            month = calendar.month_name[datetime.date.today().month]
            return render(request, 'inventory/dashboard.html', {
                'date': datetime.date.today(),
                'products': li,
                'productss': lis,
                'orders': lit,
                'month': month,
            })
        profile = get_object_or_404(BusinessProfile, pk=1)
        print("-------------",profile.c_phone)
        return render(request, 'inventory/business_profile.html',{
            'form': form,
            'profile': profile
        })


def localization(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = LocalizationForm(request.POST or None)
        print("dgxfxjfxkyjxkfyx")
        if form.is_valid():
            profile = form.save(commit=False)
            profile.c_country = form.cleaned_data.get('c_country')
            profile.c_currency = form.cleaned_data.get('c_currency')
            profile.c_timezone = form.cleaned_data.get('c_timezone')
            profile1 = get_object_or_404(Localization, pk=1)
            profile1.c_country = profile.c_country
            profile1.c_timezone = profile.c_timezone
            profile1.c_currency = profile.c_currency
            profile1.save()
            products = Product.objects.filter(user=request.user)
            orders = Order.objects.filter(user=request.user, date__year=datetime.date.today().year)
            orderss = Order.objects.filter(user=request.user, date__month=datetime.date.today().month)
            dic = {}
            for order in orderss:
                if order.status == 1:
                    ois = OInvoice.objects.filter(order=order.id)
                    for pi in ois:
                        product = Product.objects.get(pk=pi.product.id)
                        if product in dic.keys():
                            dic[product] = dic[product] + pi.quantity
                        else:
                            dic[product] = pi.quantity
            sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
            lis = []
            if len(sorted_x) > 5:
                for i in range(5):
                    lis.append(sorted_x[i][0])
            else:
                for i in range(len(sorted_x)):
                    lis.append(sorted_x[i][0])

            dic = {}
            for order in orders:
                if order.status == 1:
                    ois = OInvoice.objects.filter(order=order.id)
                    for pi in ois:
                        product = Product.objects.get(pk=pi.product.id)
                        if product in dic.keys():
                            dic[product] = dic[product] + pi.quantity
                        else:
                            dic[product] = pi.quantity
            sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
            li = []
            if len(sorted_x) > 5:
                for i in range(5):
                    li.append(sorted_x[i][0])
            else:
                for i in range(len(sorted_x)):
                    li.append(sorted_x[i][0])
            orders = Order.objects.filter(user=request.user).order_by('-date')
            print(orders)
            lit = []
            i = 0
            for order in orders:
                if i == 5:
                    break
                lit.append(order)
                i += 1

            month = calendar.month_name[datetime.date.today().month]
            return render(request, 'inventory/dashboard.html', {
                'date': datetime.date.today(),
                'products': li,
                'productss': lis,
                'orders': lit,
                'month': month,
            })
        profile = get_object_or_404(Localization, pk=1)
        print ("-----------------", profile.c_currency)
        return render(request, 'inventory/localization.html', {
            'form': form,
            'profile': profile,
        })


def new_purchase(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        purchase = Purchase.objects.filter(user=request.user).aggregate(Max('id'))
        value1 = purchase.get('id__max')
        print(value1)
        if value1 is None:
            value = 1
        else:
            value = value1 + 1
        suppliers = Supplier.objects.filter(user=request.user)
        return render(request, 'inventory/new_purchase.html',{
            'suppliers': suppliers,
            'value': value,
            'date': datetime.date.today(),
        })


def new_purchase_purchase(request,purchase_id):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = IDForm(request.POST or None)
        if form.is_valid():
            p = form.save(commit=False)
            p.id = form.cleaned_data.get('id')

            print("=================",p.id,purchase_id)
            product = Product.objects.get(id=p.id)
            purchase = Purchase.objects.filter(id = purchase_id)
            print(purchase)
            if not purchase:
                purchase = Purchase.objects.create(id= purchase_id,user=request.user, supplier=product.supplier, date= datetime.date.today(), total=0)
            else:
                purchase = Purchase.objects.get(id = purchase_id)
            s = Supplier.objects.filter(id=product.supplier.id)
            for pur in purchase.items.all():
                if pur.id == p.id:
                    return render(request, 'inventory/new_purchase.html', {
                        'suppliers': s,
                        'value': purchase_id,
                        'products': purchase.items.all(),
                        'pis': purchase.pinvoice_set.all(),
                    })
            pi = PInvoice(product=product, purchase=purchase, quantity=1, subtotal=product.cost_price, product_name=product.product_name)
            pi.save()
            print(purchase.pinvoice_set.all())
            print(purchase.items.all())
            return render(request, 'inventory/new_purchase.html',{
                'suppliers': s,
                'value': purchase_id,
                'products': purchase.items.all(),
                'pis': purchase.pinvoice_set.all(),
                'date': purchase.date,
            })
        return render(request,'inventory/localization.html')


def purchase_invoice(request, purchase_id):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        quantities = request.POST.getlist('quantities')
        pis = PInvoice.objects.filter(purchase=purchase_id)
        i=0
        total = 0
        print(quantities)
        for pi in pis:
            pi.quantity = quantities[i]
            print(pi.quantity)
            product = Product.objects.get(pk=pi.product.id)
            product.quantity = product.quantity + int(pi.quantity)
            product.save()
            pi.subtotal = float(pi.quantity) * float(product.cost_price)
            total = total+pi.subtotal
            pi.save()
            i=i+1
        dashboard = Dashboard.objects.get(pk=1)
        purchase = Purchase.objects.get(pk=purchase_id)
        purchase.total = total
        dashboard.stock = float(dashboard.stock)+float(purchase.total)
        dashboard.save()
        purchase.save()
        supplier = Supplier.objects.get(pk=purchase.supplier.id)
        items = purchase.items.all()
        return render(request,'inventory/purchase_invoice.html',{
            'purchase': purchase,
            'supplier': supplier,
            'user': request.user,
            'items': items,
        })


def invoice(request, purchase_id):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        purchase = Purchase.objects.get(pk=purchase_id)
        supplier = Supplier.objects.get(pk=purchase.supplier.id)
        items = purchase.items.all()
        return render(request,'inventory/purchase_invoice.html',{
            'purchase': purchase,
            'supplier': supplier,
            'user': request.user,
            'items': items,
        })


def manage_purchase(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        purchase = Purchase.objects.filter(user=request.user)
        return render(request, 'inventory/manage_purchase.html', {
            'purchases': purchase,
            'user': request.user,
        })


def view_product(request,product_id):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        product =Product.objects.get(pk=product_id);
        return render(request,'inventory/view_product.html',{
            'product':product,
        })


def stock_report(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        stock = Product.objects.filter(user=request.user)
        return render(request,'inventory/stock_report.html',{
            'stock': stock,
        })


def new_order(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        order = Order.objects.filter(user=request.user).aggregate(Max('id'))
        value1 = order.get('id__max')
        print(value1)
        if value1 is None:
            value = 1
        else:
            value = value1 + 1
        products = Product.objects.filter(user=request.user)
        return render(request, 'inventory/new_order.html',{
            'value': value,
            'date': datetime.date.today(),
            'products': products,
        })


def new_order_order(request,order_id):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = IDForm(request.POST or None)
        if form.is_valid():
            p = form.save(commit=False)
            p.id = form.cleaned_data.get('id')

            print("=================",p.id,order_id)
            product = Product.objects.get(id=p.id)
            print(product.s_date,datetime.date.today(),product.e_date)
            if datetime.date.today()>= product.s_date and datetime.date.today() <= product.e_date:
                product.offer = 1
            product.save()
            print(product.offer)
            order = Order.objects.filter(id = order_id)
            print(order)
            if not order:
                order = Order.objects.create(id= order_id,user=request.user, date= datetime.date.today(), total=0, status=0 ,profit=0)
            else:
                order = Order.objects.get(id = order_id)
            for ord in order.items.all():
                if ord.id == p.id:
                    return render(request, 'inventory/new_order.html', {
                        'value': order_id,
                        'products': order.items.all(),
                        'ois': order.oinvoice_set.all(),
                        'oproducts': order.items.all(),
                    })
            if product.offer:
                oi = OInvoice(product=product, order=order, quantity=1, subtotal=product.price,
                              product_name=product.product_name)
            else:
                oi = OInvoice(product=product, order=order, quantity=1, subtotal=product.selling_price, product_name=product.product_name)
            oi.save()
            print(order.oinvoice_set.all())
            print(order.items.all())
            products = Product.objects.filter(user=request.user)
            return render(request, 'inventory/new_order.html',{
                'value': order_id,
                'oproducts': order.items.all(),
                'ois': order.oinvoice_set.all(),
                'products': products,
                'date': order.date,
            })
        return render(request,'inventory/new_order.html',{
            'form': form,
        })


def checkout(request, order_id):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        quantities = request.POST.getlist('quantitie')
        ois = OInvoice.objects.filter(order=order_id)
        i = 0
        total = 0
        cost = 0
        print(quantities)
        for pi in ois:
            pi.quantity = quantities[i]
            print(pi.quantity)
            product = Product.objects.get(pk=pi.product.id)
            if product.offer:
                pi.subtotal = float(pi.quantity) * float(product.price)
            else:
                pi.subtotal = float(pi.quantity) * float(product.selling_price)
            cost+= float(pi.quantity) * float(product.cost_price)
            print("cost ",cost)
            total = total + pi.subtotal
            pi.save()
            i = i + 1

        order = Order.objects.get(pk=order_id)
        order.total = total
        order.profit = total-cost
        order.save()
        customers = Customer.objects.filter(user=request.user)
        items = order.items.all()
        return render(request, 'inventory/checkout.html', {
            'order': order,
            'customers': customers,
            'user': request.user,
            'items': items,
            'value': order_id,
        })


@csrf_exempt
def get_discount(request):
    sclist = []
    response = {'msg': 'Yes', 'status': '1'}
    json_request = json.loads(request.body)
    customer = json_request.get('customer', 'All')
    cust = Customer.objects.get(pk= customer)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=",cust.id,)
    dc = {"discount": cust.discount, "address": cust.address}
    sclist.append(dc)
    response.update({'list': sclist})
    return JsonResponse(response)


def order_invoice(request, order_id ):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = IDForm(request.POST or None)
        if form.is_valid():
            p = form.save(commit=False)
            p.id = form.cleaned_data.get('id')
            customer = Customer.objects.get(pk=p.id)
            order = Order.objects.get(pk=order_id)
            order.customer = customer
            order.profit = float(order.profit) - float(order.total)*(float(customer.discount)*0.01)
            ois = OInvoice.objects.filter(order=order_id)
            for pi in ois:
                product = Product.objects.get(pk=pi.product.id)
                product.quantity = product.quantity - int(pi.quantity)
                product.save()
            order.status = 1
            order.save()
            dashboard= Dashboard.objects.get(pk=1)
            dashboard.sales +=1
            dashboard.revenue = float(dashboard.revenue) + (float(order.total)*(1-float(customer.discount)*0.01))
            dashboard.profit = float(dashboard.profit) + float(order.profit)
            dashboard.save()
            profile = BusinessProfile.objects.get(pk=1)
            localization = Localization.objects.get(pk=1)
            return render(request, 'inventory/order_invoice.html',{
                "order": order,
                "customer": customer,
                "user": request.user,
                "items": order.items.all(),
                "profile": profile,
                "localization": localization
            })
        return render(request, 'inventory/localization.html')


def manage_order(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        order = Order.objects.filter(user=request.user)
        return render(request, 'inventory/manage_order.html', {
            'orders': order,
            'user': request.user,
        })


def ordinvoice(request, order_id):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        order = Order.objects.get(pk=order_id)
        customer = Customer.objects.get(pk=order.customer.id)
        items = order.items.all()
        profile = BusinessProfile.objects.get(pk=1)
        localization = Localization.objects.get(pk=1)
        return render(request, 'inventory/order_invoice.html', {
            "order": order,
            "customer": customer,
            "user": request.user,
            "items": order.items.all(),
            "profile": profile,
            "localization": localization
        })


def sales_report1(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        orders = Order.objects.filter(date__range=["2017-12-12","2017-12-12"])
        return render(request, 'inventory/sales_report.html', {
            'orders': orders,
        })


def sales_report(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = SalesForm(request.POST or None)
        print("afgjifj")
        if form.is_valid():
            p = form.save(commit=False)
            p.start_date = form.cleaned_data.get('start_date')
            print(p.start_date)
            p.end_date = form.cleaned_data.get('end_date')
            print(p.end_date)
            orders = Order.objects.filter(date__range=[p.start_date,p.end_date])
            print(orders)
            profile = BusinessProfile.objects.get(pk=1)
            localization = Localization.objects.get(pk=1)
            return render(request, 'inventory/sales_report.html', {
                "orders": orders,
                "start_date": p.start_date,
                "end_date": p.end_date,
            "profile": profile,
            "localization": localization
            })
        print("sxdfghjkzsdfghjksdfghjk")
        return render(request, 'inventory/sales_report.html', {
            'form': form,
        })


def sales_summary_report1(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        orders = Order.objects.filter(date__range=["2017-12-12","2017-12-12"])
        return render(request, 'inventory/sales_summary_report.html', {
            'orders': orders,
        })


def sales_summary_report(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = SalesForm(request.POST or None)
        print("afgjifj")
        if form.is_valid():
            p = form.save(commit=False)
            p.start_date = form.cleaned_data.get('start_date')
            print(p.start_date)
            p.end_date = form.cleaned_data.get('end_date')
            print(p.end_date)
            orders = Order.objects.filter(date__range=[p.start_date,p.end_date])
            print(orders)
            return render(request, 'inventory/sales_summary_report.html', {
                "orders": orders,
                "start_date": p.start_date,
                "end_date": p.end_date,
            })
        print("sxdfghjkzsdfghjksdfghjk")
        return render(request, 'inventory/sales_summary_report.html', {
            'form': form,
        })


def purchase_report1(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        purchases = Purchase.objects.filter(date__range=["2017-12-12","2017-12-12"])
        return render(request, 'inventory/purchase_report.html', {
            'purchases': purchases,
        })


def purchase_report(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        form = SalesForm(request.POST or None)
        print("afgjifj")
        if form.is_valid():
            p = form.save(commit=False)
            p.start_date = form.cleaned_data.get('start_date')
            print(p.start_date)
            p.end_date = form.cleaned_data.get('end_date')
            print(p.end_date)
            purchases = Purchase.objects.filter(date__range=[p.start_date,p.end_date])
            print(purchases)
            profile = BusinessProfile.objects.get(pk=1)
            localization = Localization.objects.get(pk=1)
            return render(request, 'inventory/purchase_report.html', {
                "purchases": purchases,
                "start_date": p.start_date,
                "end_date": p.end_date,
            "profile": profile,
            "localization": localization
            })
        print("sxdfghjkzsdfghjksdfghjk")
        return render(request, 'inventory/purchase_report.html', {
            'form': form,
        })


def notification(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        products = Product.objects.filter(user=request.user)
        p=[]
        for product in products:
            if product.quantity <= product.notify_quantity:
                p.append(product)

        return render(request,'inventory/notification.html',{
            'products': p,
        })


def cancelled_order(request):
    if not request.user.is_authenticated():
        return render(request, 'inventory/login.html')
    else:
        orders = Order.objects.filter(user=request.user)
        p=[]
        for order in orders:
            if order.status==0:
                p.append(order)

        return render(request,'inventory/cancelled_order.html',{
            'orders': p,
        })


def submit(request):
    return render(request,'inventory/submit.html')