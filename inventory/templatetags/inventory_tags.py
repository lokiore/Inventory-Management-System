from django import template
from inventory.models import Product, Purchase, PInvoice, OInvoice, Order
import datetime
register = template.Library()


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price


@register.simple_tag()
def getquantity(purchase, item):
    pi = PInvoice.objects.get(purchase=purchase.id, product=item.id)
    print(pi.quantity)
    return pi.quantity


@register.simple_tag()
def getquantity1(order, item):
    pi = OInvoice.objects.get(order=order.id, product=item.id)
    print(pi.quantity)
    return pi.quantity


@register.simple_tag()
def getsubtotal(purchase, item):
    pi = PInvoice.objects.get(purchase=purchase.id, product=item.id)
    return pi.subtotal


@register.simple_tag()
def getsubtotal1(order, item):
    pi = OInvoice.objects.get(order=order.id, product=item.id)
    return pi.subtotal


@register.simple_tag()
def getdiscount(customer,total):
    return float(total)*(float(customer.discount)*0.01)


@register.simple_tag()
def getgrand(customer,total):
    return float(total)*(1-float(customer.discount)*0.01)

@register.simple_tag()
def gettotal(subtotal, discount):
    di = discount[0].discount
    return subtotal*(1-di*0.01)


@register.simple_tag()
def gettotal1(subtotal, discount):
    return subtotal*(1-discount*0.01)

@register.simple_tag()
def getcost(order):
    cost=0.0
    total=0.0
    ois = OInvoice.objects.filter(order=order.id)
    for pi in ois:
        product = Product.objects.get(pk=pi.product.id)
        if product.offer == 0:
            pi.subtotal = float(pi.quantity) * float(product.selling_price)
        else:
            pi.subtotal = float(pi.quantity) * float(product.price)
        cost += float(pi.quantity) * float(product.cost_price)
        total = total + pi.subtotal
        pi.save()
    return cost


@register.simple_tag()
def getprice(order):
    cost=0.0
    total=0.0
    ois = OInvoice.objects.filter(order=order.id)
    for pi in ois:
        product = Product.objects.get(pk=pi.product.id)
        if product.offer == 0:
            pi.subtotal = float(pi.quantity) * float(product.selling_price)
        else:
            pi.subtotal = float(pi.quantity) * float(product.price)
        cost += float(pi.quantity) * float(product.cost_price)
        total = total + pi.subtotal
    return total


@register.simple_tag()
def getcostt(orders):
    costt=0.0
    for order in orders:
        cost = 0.0
        ois = OInvoice.objects.filter(order=order.id)
        for pi in ois:
            product = Product.objects.get(pk=pi.product.id)
            cost += float(pi.quantity) * float(product.cost_price)
        costt+=cost
    return costt


@register.simple_tag()
def getrevenue(orders):
    revenue=0.0
    for order in orders:
        if order.status==1:
            total = 0.0
            ois = OInvoice.objects.filter(order=order.id)
            for pi in ois:
                product = Product.objects.get(pk=pi.product.id)
                if product.offer == 0:
                    pi.subtotal = float(pi.quantity) * float(product.selling_price)
                else:
                    pi.subtotal = float(pi.quantity) * float(product.price)
                total = total + pi.subtotal
            revenue = revenue+( total*(1- float(order.customer.discount*0.01)) )

    return revenue


@register.simple_tag()
def getprofit(orders):
    profit=0.0
    for order in orders:
        profit += float(order.profit)
    return profit


@register.simple_tag()
def getre(user,month):
    orders = Order.objects.filter(user=user, date__month=month)
    revenue = 0.0
    for order in orders:
        if order.status==1:
            total = 0.0
            ois = OInvoice.objects.filter(order=order.id)
            for pi in ois:
                product = Product.objects.get(pk=pi.product.id)
                if product.offer == 0:
                    pi.subtotal = float(pi.quantity) * float(product.selling_price)
                else:
                    pi.subtotal = float(pi.quantity) * float(product.price)
                total = total + pi.subtotal
            revenue = revenue + (total * (1 - float(order.customer.discount * 0.01)))

    return revenue


@register.simple_tag()
def getpr(user,month):
    orders = Order.objects.filter(user=user, date__month=month)
    profit = 0.0
    for order in orders:
        if order.status==1:
            profit += float(order.profit)
    return profit


@register.simple_tag()
def getrev(user):
    orders = Order.objects.filter(user=user)
    revenue = 0.0
    for order in orders:
        if order.status==1:
            total = 0.0
            ois = OInvoice.objects.filter(order=order.id)
            for pi in ois:
                product = Product.objects.get(pk=pi.product.id)
                if product.offer == 0:
                    pi.subtotal = float(pi.quantity) * float(product.selling_price)
                else:
                    pi.subtotal = float(pi.quantity) * float(product.price)
                total = total + pi.subtotal
            revenue = revenue + (total * (1 - float(order.customer.discount * 0.01)))

    return revenue


@register.simple_tag()
def getpro(user):
    orders = Order.objects.filter(user=user)
    profit = 0.0
    for order in orders:
        if order.status==1:
            profit += float(order.profit)
    return profit



@register.simple_tag()
def getpu(user,month):
    purchases = Purchase.objects.filter(user=user , date__month=month)
    cost = 0.0
    for purchase in purchases:
        total = 0.0
        pis = PInvoice.objects.filter(purchase=purchase.id)
        for pi in pis:
            product = Product.objects.get(pk=pi.product.id)
            pi.subtotal = float(pi.quantity) * float(product.cost_price)
            total = total + pi.subtotal
        cost += total

    return cost


@register.simple_tag()
def getstock(user):
    products =Product.objects.filter(user=user)
    stock=0.0
    for product in products:
        stock += float(product.quantity)*float(product.cost_price)
    return stock


@register.simple_tag()
def getsales(user):
    orders=Order.objects.filter(user=user)
    a=0
    for order in orders:
        if order.status==1:
            a+=1

    return a


@register.simple_tag()
def getreq(user):
    orders = Order.objects.filter(user=user, date=datetime.date.today())
    revenue = 0.0
    for order in orders:
        if order.status==1:
            total = 0.0
            ois = OInvoice.objects.filter(order=order.id)
            for pi in ois:
                product = Product.objects.get(pk=pi.product.id)
                if product.offer == 0:
                    pi.subtotal = float(pi.quantity) * float(product.selling_price)
                else:
                    pi.subtotal = float(pi.quantity) * float(product.price)
                total = total + pi.subtotal
            revenue = revenue + (total * (1 - float(order.customer.discount * 0.01)))

    return revenue


@register.simple_tag()
def getrep(user,year):
    orders = Order.objects.filter(user=user, date__year=year)
    revenue = 0.0
    for order in orders:
        if order.status==1:
            total = 0.0
            ois = OInvoice.objects.filter(order=order.id)
            for pi in ois:
                product = Product.objects.get(pk=pi.product.id)
                if product.offer == 0:
                    pi.subtotal = float(pi.quantity) * float(product.selling_price)
                else:
                    pi.subtotal = float(pi.quantity) * float(product.price)
                total = total + pi.subtotal
            revenue = revenue + (total * (1 - float(order.customer.discount * 0.01)))

    return revenue


@register.simple_tag()
def getnumber(user):
    products = Product.objects.filter(user=user)
    i=0
    for product in products:
        if product.quantity <= product.notify_quantity:
            i+=1
    return i


@register.simple_tag()
def getcancelled(user):
    orders = Order.objects.filter(user=user)
    i=0
    for order in orders:
        if order.status == 0:
            i+=1

    return i