from django.db import models
from users.models import User

class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="merchant")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=500, blank=False )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantPlan(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    product_listings = models.IntegerField(blank=False, default=0)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantPlanPrice(models.Model):
    merchant_plan = models.ForeignKey(MerchantPlan, on_delete=models.CASCADE, related_name="prices")
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=True, null=True)
    price = models.IntegerField(blank=False, default=0)
    stripe_price_key = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantPlanFeature(models.Model):
    merchant_plan = models.ForeignKey(MerchantPlan, on_delete=models.CASCADE, related_name="features")
    title = models.CharField(max_length=500, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantSubcription(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE, related_name="subscription")
    merchant_plan = models.ForeignKey(MerchantPlan, on_delete=models.CASCADE, related_name="subscribers")
    stripe_sub_id = models.CharField(max_length=200, blank=False, default='')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantStore(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="stores")
    uid = models.CharField(max_length=20, blank=True, unique=True)
    stripe_account_id = models.CharField(max_length=120, blank=True, unique=True)
    name = models.CharField(max_length=500, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    logo = models.ImageField(upload_to="images/merchant_store_media/logos/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="images/merchant_store_media/banners/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantStoreView(models.Model):
    merchant_store = models.ForeignKey(MerchantStore, on_delete=models.CASCADE, related_name="views")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantStoreCategory(models.Model):
    merchant_store = models.ForeignKey(MerchantStore, on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    banner_image = models.ImageField(upload_to="images/merchant_store_media/categories/banners/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantStoreCategoryView(models.Model):
    merchant_store_category = models.ForeignKey(MerchantStoreCategory, on_delete=models.CASCADE, related_name="views", default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantPaymentMethod(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="payment_methods", default='')
    stripe_pm_id = models.CharField(max_length=120, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)