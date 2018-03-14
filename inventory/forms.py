from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import User1, Supplier, Product, Category, SubCategory, Customer, BusinessProfile, ID, Date, Localization

class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, max_length=10)
    username = forms.CharField(max_length=100)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


'''
class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']'''


class AddSupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ['company_name', 'supplier_name', 'email', 'phone_number', 'address']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['product_category']


class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = ['product_category', 'product_subcategory']


class AddProductForm(forms.ModelForm):
    s_date = forms.DateField(input_formats=['%Y/%m/%d', '%m/%d/%Y', '%m/%d/%y'])
    e_date = forms.DateField(input_formats=['%Y/%m/%d', '%m/%d/%Y', '%m/%d/%y'])

    class Meta:
        model = Product
        fields = ['product_code', 'product_name', 'supplier', 'product_category', 'product_subcategory', 'cost_price', 'selling_price', 'notify_quantity' ,'s_date', 'e_date','price' ]


class AddCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number', 'discount', 'address']


class BusinessProfileForm(forms.ModelForm):

    class Meta:
        model = BusinessProfile
        fields = ['c_name', 'c_email', 'c_address', 'c_phone', 'c_logo']


class LocalizationForm(forms.ModelForm):

    class Meta:
        model = Localization
        fields = ['c_country', 'c_currency', 'c_timezone']


class IDForm(forms.ModelForm):

    class Meta:
        model = ID
        fields = ['id',]


class SalesForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=['%Y/%m/%d', '%m/%d/%Y', '%m/%d/%y'])
    end_date = forms.DateField(input_formats=['%Y/%m/%d', '%m/%d/%Y', '%m/%d/%y'])

    class Meta:
        model = Date
        fields = ['start_date', 'end_date']