from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    uid = models.CharField(max_length=20, blank=False, unique=True)
    agreed_to_toa = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=False)
    gender = models.CharField(blank=False)
    stripe_customer_id = models.CharField(max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

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

class UserGenderChoice(models.Model):
    gender = models.CharField(blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserGenderChoiceSelected(models.Model):
    user_gender_choice = models.ForeignKey(UserGenderChoice, on_delete=models.CASCADE, related_name="choices_selected")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gender_choice_selected")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(blank=False)
    phone_number = models.CharField(blank=False)
    street_address = models.CharField(max_length=1000, blank=False)
    street_address_ext = models.CharField(max_length=1000, blank=True)
    city = models.CharField(blank=False)
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class UserLogin(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='logins')
    ip_address = models.CharField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    state = models.CharField(blank=True, null=True)
    country_code = models.CharField(blank=True, null=True)
    zipcode = models.CharField(blank=True, null=True)
    device = models.CharField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)
