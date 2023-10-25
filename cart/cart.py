from decimal import Decimal
from django.conf import settings

from main_page.models import Product
from coupons.models import Coupon


class Cart(object):
    """
    initiating the cart
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            """
            here we are saving our empty cart in the session
            """
            cart = self.session[settings.CART_SESSION_ID] = {

            }
        self.cart = cart
        """saving our new coupon"""
        self.coupon_id = self.session.get('coupon_id')

    def add_products_to_cart(self, product, quantity=1, override_quantity=False):
        """
        Adding new products to the cart or updating quantity
        :param product: instance of our product model
        :param quantity: integer with the quantity of the product
        :param override_quantity: boolean, do we need to override quantity (when we need more than 1 product)
        or to keep quantity at 1
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save_cart()

    def save_cart(self):
        """
        we need to set our session as 'modified' to save it
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove_product(self, product):
        """
        removing products from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_cart()

    def __iter__(self, product_id=None):
        """
        this func scrolling through the products in the cart and getting other
        products from the database
        :param product_id: key in the dict of the cart
        """
        product_ids = self.cart.keys()
        """
        receiving products and adding them to the cart
        """
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        counting quantity of all products in our cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        counting the total price of all products in our cart
        """
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear_the_cart(self):
        """
        this method clearing the session of the cart
        """
        del self.session[settings.CART_SESSION_ID]
        self.save_cart()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
