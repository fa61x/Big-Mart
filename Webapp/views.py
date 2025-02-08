from django.shortcuts import render, redirect
from Backend.models import ProductDB, categoriesDB
from Webapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import razorpay


# Create your views here.
def home_page(req):
    cat = categoriesDB.objects.all()
    return render(req, "Home.html", {'cat': cat})


def about_page(req):
    cat = categoriesDB.objects.all()
    return render(req, "About.html", {'cat': cat})


def contact_page(req):
    cat = categoriesDB.objects.all()
    return render(req, "Contact.html", {'cat': cat})


def blog_page(req):
    cat = categoriesDB.objects.all()
    return render(req, "Blog.html", {'cat': cat})


def shop_page(req):
    shop_data = ProductDB.objects.all()
    cat = categoriesDB.objects.all()
    return render(req, "Shop.html", {'shop_data': shop_data, 'cat': cat})


def feedback_page(request):
    if request.method == "POST":
        na = request.POST.get('cname')
        em = request.POST.get('CEmail')
        sub = request.POST.get('c_subject')
        mes = request.POST.get('c_message')
        obj3 = ContactDB(Name=na, Email=em, Subject=sub, Message=mes)
        obj3.save()
    return redirect(contact_page)


def Product_filteredpage(req, cat_name):
    data = ProductDB.objects.filter(Category=cat_name)
    cat = categoriesDB.objects.all()
    return render(req, "Product_filtered.html", {'data': data, 'cat': cat})


def single_product(req, p_id):
    cat = categoriesDB.objects.all()
    data = ProductDB.objects.get(id=p_id)
    return render(req, "Single_product.html", {'data': data, 'cat': cat})


######################################################################################################
def user_register(request):
    return render(request, "Register.html")


def user_save_register(request):
    if request.method == "POST":
        un = request.POST.get('username')
        em = request.POST.get('email_id')
        pas = request.POST.get('password')
        obj = RegisterDB(UserName=un, UserEmail=em, UserPassword=pas)
        if RegisterDB.objects.filter(UserName=un).exists():
            messages.warning(request, "Username already Exists")
            return redirect(user_register)
        elif RegisterDB.objects.filter(UserEmail=em).exists():
            messages.warning(request, "Email_id already Exists")
        else:
            obj.save()
            messages.success(request, "User Registered ")
            return redirect(user_register)


def User_Login(request):
    if request.method == "POST":
        un = request.POST.get('uname')
        ps = request.POST.get('pwd')
        if RegisterDB.objects.filter(UserName=un, UserPassword=ps).exists():
            request.session['Username'] = un
            request.session['Password'] = ps
            messages.success(request, "WELCOME")
            return redirect(home_page)
        else:
            messages.error(request, "Invalid Username!")
            return redirect(user_login_page)
    else:
        messages.warning(request, "User not found!")
        return redirect(user_login_page)


def User_logout(request):
    del request.session['Username']
    del request.session['Password']
    messages.success(request, "Logout Successfully")
    return redirect(home_page)


def cart_save(request):
    if request.method == "POST":
        cu = request.POST.get('ct_u')
        cp = request.POST.get('ct_pname')
        cq = request.POST.get('ct_qty')
        ct = request.POST.get('ct_total')
        obj = cartDB(Ct_username=cu, Ct_Product_Name=cp, Ct_Quantity=cq, Ct_Total_Price=ct)
        obj.save()
        return redirect(home_page)


def cart_page(request):
    cat = categoriesDB.objects.all()
    cart_data = cartDB.objects.filter(Ct_username=request.session['Username'])
    sub_total = 0
    delivery_charges = 0
    total = 0
    for i in cart_data:
        sub_total = sub_total + i.Ct_Total_Price
        if sub_total >= 500:
            delivery_charges = 50
        else:
            delivery_charges = 100
        total = sub_total + delivery_charges
    return render(request, "Cart.html",
                  {'cat': cat, 'cart_data': cart_data, 'sub_total': sub_total, 'delivery_charges': delivery_charges,
                   'total': total})


def check_out_page(request):
    cat = categoriesDB.objects.all()
    products = cartDB.objects.filter(Ct_username=request.session['Username'])
    sub_total = delivery_charges = total = 0
    for i in products:
        sub_total = sub_total + i.Ct_Total_Price
        if sub_total >= 500:
            delivery_charges = 50
        else:
            delivery_charges = 100
        total = sub_total + delivery_charges

    return render(request, "Check_Out.html", {'products': products, 'sub_total': sub_total,
                                              'delivery_charges': delivery_charges, 'total': total, 'cat': cat})


def user_login_page(request):
    return render(request, "User_login.html")


def delete_cart_page(request, c_id):
    x = cartDB.objects.filter(id=c_id)
    x.delete()
    return redirect(cart_page)


def payment_page(request):
    customer = orderDB.objects.order_by('-id').first()
    payy = customer.Order_Price
    amount = int(payy*100)
    payy_str = str(amount)
    for i in payy_str:
        print(i)
    if request.method == "POST":
        order_currency = 'INR'
        client = razorpay.Client()
    return render(request, "Payment.html",{'customer':customer})


def save_order(request):
    if request.method == "POST":
        orn = request.POST.get('Or_name')
        ors = request.POST.get('Or_state')
        ora = request.POST.get('Or_address')
        orp = request.POST.get('Or_mob')
        ore = request.POST.get('Or_email')
        orep = request.POST.get('Or_price')
        obj = orderDB(Order_Name=orn,Order_State=ors,Order_Address=ora,
                      Order_Number=orp,Order_Email=ore,Order_Price=orep)
        obj.save()
        return redirect(payment_page)
