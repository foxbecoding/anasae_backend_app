from django.db import models
from users.models import User
from merchants.models import MerchantStore
from products.models import Product, ProductVariantItem

class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
  created = models.DateTimeField(auto_now_add=True, null=True)
  updated = models.DateTimeField(auto_now_add=True, null=True)
  deleted = models.DateTimeField(null=True)

class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
  merchant_store = models.ForeignKey(MerchantStore, on_delete=models.SET_NULL, related_name="orders", null=True)
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="orders", null=True)
  product_variant_item = models.ForeignKey(ProductVariantItem, on_delete=models.CASCADE, related_name="orders", blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True, null=True)
  updated = models.DateTimeField(auto_now_add=True, null=True)
  deleted = models.DateTimeField(null=True)

class OrderItemFulfillment(models.Model):
  order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name="items")
  shipping_label = models.CharField(blank=True, null=True)
  is_shipped = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True, null=True)
  updated = models.DateTimeField(auto_now_add=True, null=True)
  deleted = models.DateTimeField(null=True)
