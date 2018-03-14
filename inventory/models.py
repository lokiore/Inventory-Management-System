from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import Permission, User


class User1(models.Model):
    user = models.ForeignKey(User, default=1)
    username = models.CharField(max_length=15, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    password1 = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone_regex = RegexValidator(regex=r'^(+91)?[1-9][0-9]{9}$',
                                 message="Phone number must be entered in the format: '+91##########'.")
    phone_number = models.IntegerField()

    def __str__(self):
        return self.username


class Supplier(models.Model):
    user = models.ForeignKey(User, default=1)

    company_name = models.CharField(max_length=100, unique=True , default="")
    supplier_name = models.CharField(max_length=100 , default="")
    email = models.EmailField(max_length=100 , default="")
    phone_regex = RegexValidator(regex=r'^[1-9][0-9]{9}$',
                                 message="Phone number must be entered in the format: '+91##########'.",
                                 code='invalid_username')
    phone_number = models.IntegerField(default="" , validators=[phone_regex])
    address = models.CharField(max_length=250 , default="")

    def __str__(self):
        return self.company_name + ' - ' + self.supplier_name


class Tax(models.Model):
    user = models.ForeignKey(User, default=1)
    tax_name = models.CharField(max_length=20)
    tax_value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=0)

    def __str__(self):
        return self.tax_name


class Category(models.Model):
    user = models.ForeignKey(User, default=1)
    product_category = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.product_category


class SubCategory(models.Model):
    product_subcategory = models.CharField(max_length=100)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.product_subcategory


class Product(models.Model):
    product_code = models.CharField(max_length=10, unique=True)
    product_name = models.CharField(max_length=100 , default="")
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product_subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_image = models.FileField()
    cost_price = models.DecimalField(max_digits=8, decimal_places=2)
    selling_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=0)
    notify_quantity = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, default=1)
    user = models.ForeignKey(User, default=1)
    s_date = models.DateField(null=True)
    e_date = models.DateField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    offer = models.IntegerField(default=0)
    def __str__(self):
        return self.product_code + ' - ' + self.product_name


class Customer(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=100, default="", unique=True)
    email = models.EmailField(max_length=100, default="")
    phone_regex = RegexValidator(regex=r'^[1-9][0-9]{9}$',
                                 message="Phone number must be entered in the format: '##########'.",code='invalid_username')
    phone_number = models.IntegerField(validators = [phone_regex], default="")
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    address = models.CharField(max_length=250, default="")

    def __str__(self):
        return self.name



class BusinessProfile(models.Model):
    user = models.ForeignKey(User, default=1)
    c_name = models.CharField(max_length=100, default="")
    c_email = models.EmailField(max_length=100, default="")
    c_address = models.CharField(max_length=100, default="")
    phone_regex = RegexValidator(regex=r'^[1-9][0-9]{9}$',
                                 message="Phone number must be entered in the format: '##########'.",
                                 code='invalid_username')
    c_phone = models.IntegerField(validators=[phone_regex])
    c_logo = models.FileField()

    def __str__(self):
        return self.c_name

class Localization(models.Model):
    user = models.ForeignKey(User , default=1)
    c_country = models.CharField(max_length=100, default="qwe")
    c_currency = models.CharField(max_length=1, default="$")
    c_timezone = models.CharField(max_length=100, default="wer")

    def __str__(self):
        return self.c_country


class Purchase(models.Model):
    user = models.ForeignKey(User,default=1)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    items = models.ManyToManyField(Product,through='PInvoice')

    def __str__(self):
        return 'PUR' + str(self.id)


class PInvoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    product_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.purchase_id) + str(self.product_id)


class ID(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.id)


class Date(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.start_date) + " " + str(self.end_date)


class Dashboard(models.Model):
    stock = models.DecimalField(max_digits=8, decimal_places=2)
    revenue = models.DecimalField(max_digits=8, decimal_places=2)
    profit = models.DecimalField(max_digits=8, decimal_places=2)
    sales = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey(User,default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.IntegerField()
    items = models.ManyToManyField(Product,through='OInvoice')
    profit = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return 'ORD' + str(self.id)


class OInvoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    product_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.order_id) + str(self.product_id)