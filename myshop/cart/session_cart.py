from .models import Cart, CartItem


class SessionCart(object):
    def __init__(self, request):
        self.session_key = request.session.session_key
        if not self.session_key:
            request.session["session_key"] = 123
            request.session.cycle_key()
        self.session_key = request.session.session_key
        try:
            cart = Cart.objects.get(session_key=self.session_key, is_ordered=False)
        except Cart.DoesNotExist:           
            cart = Cart(session_key = self.session_key)
            
        if request.user.id and not cart.user:
            cart.user = request.user

        self.cart = cart

    def __len__(self):
        return len(self.cart)

    @property
    def items(self):        
        return self.cart.active_items

    @property
    def total_price(self):
        return self.cart.total_cost

    def clear(self):
        self.cart.clear()

    @property
    def coupon(self):
        return self.cart.coupon

    @property
    def discount(self):
        return self.cart.discount

    @property
    def total_price_after_discount(self):
        return self.cart.total_price_after_discount

    @property
    def total_discount(self):
        return self.cart.total_discount

    def add(self, product, quantity=1, update_quantity=False):
        if not self.cart.id:
            self.cart.save()
        self.cart.add(product, quantity, update_quantity)

    def set_coupon(self, code):
        if not self.cart.id:
            self.cart.save()
        self.cart.set_coupon(code)

    def remove(self, product):
        self.cart.remove(product)

    def order(self):
        self.cart.order()
