import redis

from django.conf import settings

from main_page.models import Product

"""Connecting to redis"""
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender:
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                """Searching for the other similar products"""
                """or products which clients are buying with this product"""
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id),
                              1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            """only one product"""
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                                     0, -1, desc=True)[:max_results]
        else:
            """Generating tmp key"""
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            """Deleting ids of the products for which we are giving recommendations"""
            r.zrem(tmp_key, *product_ids)
            """Gaining ids of the products by their quantity"""
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            """Deleting tmp key"""
            r.delete(tmp_key)
        suggestions_products_ids = [int(id) for id in suggestions]
        """Gaining suggested products and sorting them"""
        suggested_products = list(Product.objects.filter(
            id__in=suggestions_products_ids
        ))
        suggested_products.sort(key=lambda x: suggestions_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
