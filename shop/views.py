from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.contrib import messages
from cart.cart import Cart

def shop_view(request):
    """
    View to display the main shop page with all products.
    """
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_featured=True, is_active=True)

    context = {
        'categories': categories,
        'products': products,
        'featured_products': featured_products,
    }
    return render(request, 'shop/shop.html', context)


def product_detail_view(request, slug):
    """
    View to display details of a specific product.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = product.related_products.filter(is_active=True)[:4]  # Limit related products for display

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/single-product.html', context)


def category_view(request, slug):
    """
    View to display products by category.
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/shop.html', context)


def add_to_cart(request, slug):
    """
    View to add a specific product to the cart.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart = Cart(request)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, quantity=quantity)
        messages.success(request, f'Added {product.name} to your cart.')
        return redirect('cart:cart_detail')  # Redirect to the cart detail page
    return redirect('shop:product_detail', slug=slug)