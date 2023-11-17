from django import template
#This file contains template filters
register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False

@register.filter(name='cart_count')
def cart_count(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0

@register.simple_tag()
def multiply(price, quantity):
    return quantity * price

@register.filter(name='total_price')
def total_price(product, cart):
    sum=0
    for p in product:
        price = p.price
        qty = cart_count(p, cart)
        sum += multiply(price,qty)
    return sum

@register.filter(name='total_price_ship')
def total_price_ship(product, cart):
    sum=0
    for p in product:
        price = p.price
        qty = cart_count(p, cart)
        sum += multiply(price,qty)
    return round(sum + 5.00, 2)

