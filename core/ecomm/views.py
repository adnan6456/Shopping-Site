from django.shortcuts import render, redirect
from .models import Product, Order
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.views import loginView
from accounts.forms import UserProfileForm, SignUpForm

items = None
cart = {}

# Home Page
def homeView(request):

    return render(request, 'ecomm/index2.html')

#Products Page

def products(request):
    products = None
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_by_category(categoryID)
    else:
        products = Product.get_all_products()
    context = {
        'products':products
    }
    return render(request, 'ecomm/index.html', context)

# Product Details Page
def productView(request, id):
    if request.method == 'POST':
        to_cart = request.POST.get('to_cart')
        rem_cart = request.POST.get('rem_cart')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(to_cart)
            if quantity:
                if rem_cart:
                    if quantity <= 1:
                        cart.pop(to_cart)
                    else:
                        cart[to_cart] = quantity-1
                else:
                    cart[to_cart] = quantity+1
            else:
                cart[to_cart] = 1
        else:
            cart = {}
            cart[to_cart] = 1
        request.session['cart'] = cart
        # print(request.session['cart'])

    prod = Product.objects.get(id = id)
    context = {
        'prod': prod,
    }

    return render(request, 'ecomm/product.html', context)

# Cart Page
@login_required
def cartView(request):
    global items, cart
    if type(request.session.get('cart')) == type(None):
        request.session['cart'] = {}
        
    if request.method == 'POST':
        to_cart = request.POST.get('to_cart')
        rem_cart = request.POST.get('rem_cart')
        cart = request.session.get('cart')
        checkout_but = request.POST.get('checkout_but')
        if rem_cart:
            cart.pop(str(to_cart))
            request.session['cart']=cart
        elif checkout_but:
            products = Product.get_product_by_id(list(cart.keys()))
            # print(products)
            items = products
            return redirect('checkout')
    ids = list(request.session.get('cart').keys())
    products = Product.get_product_by_id(ids)
    context={
        'cart_prod':products
    }
    return render(request, "ecomm/cart.html", context)

# Profile Page
@login_required 
def profileView(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")
    
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    context = {
        "form" : form
    }
    return render(request,"ecomm/profile.html",context)

# Checkout page
@login_required
def checkoutView(request):
    global items, cart
    if request.method == "POST":
        user = request.user
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        card_cvv = request.POST.get('card_cvv')
        for product in items:
            order = Order(
                product = product,
                user = user,
                price = product.price,
                address = address,
                phone = phone,
                quantity = cart.get(str(product.id)),
                card_name = card_name,
                card_number = card_number,
                card_cvv = card_cvv

            )
            request.session['cart'] = {}
            order.placeOrder()
        return redirect('thankyou')

    context = {}

    return render(request, 'ecomm/checkout.html', context)

# Thank you page
@login_required
def thankyouView(request):
    context={}
    return render(request, 'ecomm/thankyou.html', context)


# Orders Page
@login_required
def orderView(request):
    user = request.user
    order = Order.objects.filter(user=user)
    context={
        'order' : order
    }
    print(order)
    return render(request, 'ecomm/orders.html', context)
