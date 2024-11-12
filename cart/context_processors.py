# cart/context_processors.py

from .cart import Cart

def cart_context(request):
    """
    Context processor to make the cart available in all templates.
    """
    cart = Cart(request)
    return {'cart': cart}
