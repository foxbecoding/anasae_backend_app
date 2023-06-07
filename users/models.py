from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.helpers import create_uid

class User(AbstractUser):
    uid = models.CharField(max_length=20, blank=True, unique=True)
    agreed_to_toa = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=False)
    stripe_customer_id = models.CharField(max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.uid = create_uid('u-')
        super(User, self).save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    name = models.CharField(max_length=500, blank=False, null=False)
    is_account_holder = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserProfileImage(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to='images/user_images', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserGender(models.Model):
    gender = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserGenderChoice(models.Model):
    user_gender = models.ForeignKey(UserGender, on_delete=models.CASCADE, related_name="choices", default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gender_choice", default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserCountry(models.Model):
    name  = models.CharField(max_length=200, blank=False, null=False, unique=True)
    code = models.CharField(max_length=10, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserCountryState(models.Model):
    user_country = models.ForeignKey(UserCountry, on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=200, blank=False, null=False)
    code = models.CharField(max_length=10, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    user_country_state = models.ForeignKey(UserCountryState, on_delete=models.SET_NULL, related_name="addresses", null=True)
    full_name = models.CharField(max_length=200, blank=False)
    phone_number = models.CharField(max_length=100, blank=False)
    street_address = models.CharField(max_length=1000, blank=False)
    street_address_ext = models.CharField(max_length=1000, blank=True)
    city = models.CharField(max_length=200, blank=False)
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserLogin(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name="logins")
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    device = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)