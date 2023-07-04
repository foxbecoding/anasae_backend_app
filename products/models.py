from django.db import models
from users.models import User
from categories.models import Category, Subcategory, SubcategorySection
from merchants.models import MerchantStore
from utils.helpers import create_uid

class Product(models.Model):
    merchant_store = models.ForeignKey(MerchantStore, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, related_name="products", blank=True, null=True)
    subcategory_section = models.ForeignKey(SubcategorySection, on_delete=models.SET_NULL, related_name="products", blank=True, null=True)
    uid = models.CharField(max_length=20, blank=True, unique=True)
    sku = models.CharField(max_length=50, blank=False, unique=True)
    isbn = models.CharField(max_length=200, blank=True, null=True, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=5000, blank=False)
    quantity = models.IntegerField(blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.uid = create_uid('p-')
        super(Product, self).save(*args, **kwargs)

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    label = models.CharField(max_length=400, blank=False)
    value = models.CharField(max_length=400, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    cover_image = models.ImageField(upload_to="images/product_media/", blank=True, null=True)
    order = models.IntegerField(blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductHighlight(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="highlights")
    text = models.CharField(max_length=1000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_views", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    title = models.CharField(max_length=250, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductVariantItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=5000, blank=False)
    quantity = models.IntegerField(blank=False)
    is_active = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductVariantItemSpecification(models.Model):
    product_variant_item = models.ForeignKey(ProductVariantItem, on_delete=models.CASCADE, related_name="specifications")
    label = models.CharField(max_length=400, blank=False)
    value = models.CharField(max_length=400, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductVariantItemImage(models.Model):
    product_variant_item = models.ForeignKey(ProductVariantItem, on_delete=models.CASCADE, related_name="images")
    cover_image = models.ImageField(upload_to="images/product_media/", blank=True, null=True)
    order = models.IntegerField(blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductVariantItemView(models.Model):
    product_variant_item = models.ForeignKey(ProductVariantItem, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_variant_item_views", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_reviews")
    comment = models.CharField(max_length=500, blank=False)
    stars = models.FloatField(blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductWishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wish_list")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class ProductWishListItem(models.Model):
    wish_list = models.ForeignKey(ProductWishList, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wish_list_items")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)