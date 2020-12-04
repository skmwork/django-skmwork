from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon
from .models import Cart, CartItem
from django.db.models import Count
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone


class SessionCart(object):

    def __init__(self, request):
        self.session_key = request.session.session_key
        coupon_id = request.session.get('coupon_id')
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
        

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        try:
            if not self.cart.id:
                self.cart.save()
            cart_item = self.cart.items.get(product_id=product.id)
            if update_quantity or cart_item.is_deleted==True:
                cart_item.quantity=quantity
            else:
                cart_item.quantity+=quantity
            if cart_item.is_deleted==True:
                cart_item.is_deleted=False

            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem(product_id=product.id, quantity=quantity, cart=self.cart, price=product.price)
            cart_item.save()


    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        cart_items = self.cart.items.filter(product_id=product.id, is_deleted=False).update(is_deleted=True);


    @property
    def items(self):        
        return self.cart.items.filter(is_deleted=False).all();
        


    def __len__(self):    
        """
        Подсчет всех товаров в корзине.
        """
        return self.items.filter(is_deleted=False).count();

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return self.cart.items.filter(is_deleted=False).aggregate(total_price=Coalesce(Sum('price'),0))["total_price"]


    def clear(self):
        cart_items = self.cart.items.update(is_deleted=True)

    def order(self):
        self.cart.items.update(is_ordered=True)
        self.cart.is_ordered=True
        self.cart.save()

    @property
    def coupon(self):
        return self.cart.coupon


    def get_discount(self):      
        if self.cart.coupon:
            return (self.cart.coupon.discount / Decimal('100')) * self.get_total_price()
        else:
            return 0

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def set_coupon(self, code):
        try:
            now = timezone.now()
            self.cart.coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            self.cart.save() 
            return True
        except Coupon.DoesNotExist:
            return False