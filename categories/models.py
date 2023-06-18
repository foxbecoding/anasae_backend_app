from django.db import models
from utils.helpers import create_uid

class Category(models.Model):
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

    # def save(self, *args, **kwargs):
    #     self.uid = create_uid('cat-')
    #     super(Category, self).save(*args, **kwargs)

class CategoryCoverImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="cover_images")
    cover_image = models.ImageField(upload_to="images/category_media/main/cover_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class CategoryBannerImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="banner_images")
    banner_image = models.ImageField(upload_to="images/category_media/main/banner_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

    # def save(self, *args, **kwargs):
    #     self.uid = create_uid('scat-')
    #     super(Category, self).save(*args, **kwargs)

class SubcategoryCoverImage(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="cover_images")
    cover_image = models.ImageField(upload_to="images/category_media/subcategories/cover_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategoryBannerImage(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="banner_images")
    banner_image = models.ImageField(upload_to="images/category_media/subcategories/banner_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategorySection(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="sections")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

    # def save(self, *args, **kwargs):
    #     self.uid = create_uid('scats-')
    #     super(SubcategorySection, self).save(*args, **kwargs)

class SubcategorySectionCoverImage(models.Model):
    subcategory_section = models.ForeignKey(SubcategorySection, on_delete=models.CASCADE, related_name="cover_images", blank=True, null=True)
    cover_image = models.ImageField(upload_to="images/category_media/subcategory_sections/cover_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategorySectionBannerImage(models.Model):
    subcategory_section = models.ForeignKey(SubcategorySection, on_delete=models.CASCADE, related_name="banner_images")
    banner_image = models.ImageField(upload_to="images/category_media/subcategory_sections/banner_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class CategoryView(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="views")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, related_name="views", blank=True, null=True)
    subcategory_section = models.ForeignKey(SubcategorySection, on_delete=models.SET_NULL, related_name="views", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class CategoryProductSpecification(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="product_specification")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class CategoryProductSpecificationItem(models.Model):
    category_product_specification = models.ForeignKey(CategoryProductSpecification, on_delete=models.CASCADE, related_name="items")
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class CategoryProductSpecificationItemOption(models.Model):
    category_product_specification_item = models.ForeignKey(CategoryProductSpecificationItem, on_delete=models.CASCADE, related_name="options")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategoryProductSpecification(models.Model):
    subcategory = models.OneToOneField(Subcategory, on_delete=models.CASCADE, related_name="product_specification")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategoryProductSpecificationItem(models.Model):
    subcategory_product_specification = models.ForeignKey(SubcategoryProductSpecification, on_delete=models.CASCADE, related_name="items")
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategoryProductSpecificationItemOption(models.Model):
    subcategory_product_specification_item = models.ForeignKey(SubcategoryProductSpecificationItem, on_delete=models.CASCADE, related_name="options")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategorySectionProductSpecification(models.Model):
    subcategory_section = models.OneToOneField(SubcategorySection, on_delete=models.CASCADE, related_name="product_specification")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategorySectionProductSpecificationItem(models.Model):
    subcategory_section_product_specification = models.ForeignKey(SubcategorySectionProductSpecification, on_delete=models.CASCADE, related_name="items")
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class SubcategorySectionProductSpecificationItemOption(models.Model):
    subcategory_section_product_specification_item = models.ForeignKey(SubcategorySectionProductSpecificationItem, on_delete=models.CASCADE, related_name="options")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)