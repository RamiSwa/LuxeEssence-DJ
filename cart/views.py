# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    """
    View to add a product to the cart or update its quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    """
    View to remove a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')



def cart_detail(request):
    """
    View to display the contents of the cart.
    """
    cart = Cart(request)
    total_price = cart.get_total_price()  # Get total price from cart instance
    return render(request, 'cart/cart.html', {'cart': cart, 'total_price': total_price})





def apply_coupon(request):
    # Placeholder logic for applying a coupon
    return redirect('cart_detail')

def checkout(request):
    # Placeholder logic for checkout
    return render(request, 'cart/checkout.html')

