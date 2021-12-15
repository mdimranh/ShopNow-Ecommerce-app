from django.db import models
from product.models import Product
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class ShopCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.user.first_name+''+self.user.last_name

    def cost(self):
        return (self.product.main_price - (self.product.main_price * self.product.discount / 100)) * self.quantity

    def product_image(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.product.image.url))
    product_image.short_description = 'Image'