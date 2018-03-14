# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Supplier,Category, Customer, Product, User1, Tax
# Register your models here.
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tax)
admin.site.register(User1)