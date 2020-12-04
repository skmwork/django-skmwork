from .session_cart import SessionCart


def cart(request):
    return {'cart': SessionCart(request)}