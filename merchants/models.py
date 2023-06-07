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
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    merchant_plan_listings = models.IntegerField(blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantPlanPrice(models.Model):
    merchant_plan = models.ForeignKey(MerchantPlan, on_delete=models.CASCADE, related_name="plan_prices")
    uid = models.CharField(max_length=20, blank=True, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=True, null=True)
    price = models.FloatField(blank=False)
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
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantStore(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="stores")
    uid = models.CharField(max_length=20, blank=True, unique=True)
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

class MerchantStoreDepartment(models.Model):
    merchant_store = models.ForeignKey(MerchantStore, on_delete=models.CASCADE, related_name="departments")
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    banner_image = models.ImageField(upload_to="images/merchant_store_media/departments/banners/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class MerchantStoreDepartmentView(models.Model):
    merchant_store_department = models.ForeignKey(MerchantStoreDepartment, on_delete=models.CASCADE, related_name="views")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)