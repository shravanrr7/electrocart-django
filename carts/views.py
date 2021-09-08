from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from carts.models import Cart, Cartitem
from django.shortcuts import get_object_or_404, redirect, render
from store.models import product
from django.contrib.auth.decorators import login_required


# Create your views here.
# private function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart =request.session.create()
    return cart


def add_cart(request,product_id):
    Product = product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    
    try:
        cart_item = Cartitem.objects.get(product=Product,cart=cart)
        cart_item.quantity +=1 
        cart_item.save()
    
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
            product=Product,
            quantity =1,
            cart= cart,
        )
        cart_item.save()
    return redirect('cart')


def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id= _cart_id(request))
    Product = get_object_or_404(product, id=product_id)
    cart_item = Cartitem.objects.get(product=Product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    Product = get_object_or_404(product, id=product_id)
    cart_item = Cartitem.objects.get(product=Product,cart=cart)
    cart_item.delete()
    return redirect('cart')





def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items=Cartitem.objects.filter(cart=cart,is_active=True)
        cart_items=Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (9*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }

    return render(request,'store/cart.html',context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)