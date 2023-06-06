from django.db import models

class Department(models.Model):
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentCoverImage(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="cover_images")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    cover_image = models.ImageField(upload_to="images/department_media/main/cover_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentBannerImage(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="banner_images")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    banner_image = models.ImageField(upload_to="images/department_media/main/banner_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSection(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="sections")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSectionCoverImage(models.Model):
    department_section = models.ForeignKey(DepartmentSection, on_delete=models.CASCADE, related_name="cover_images")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    cover_image = models.ImageField(upload_to="images/department_media/sections/cover_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSectionBannerImage(models.Model):
    department_section = models.ForeignKey(DepartmentSection, on_delete=models.CASCADE, related_name="banner_images")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    banner_image = models.ImageField(upload_to="images/department_media/sections/banner_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSubSection(models.Model):
    department_section = models.ForeignKey(DepartmentSection, on_delete=models.CASCADE, related_name="sub_sections")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSubSectionCoverImage(models.Model):
    department_sub_section = models.ForeignKey(DepartmentSubSection, on_delete=models.CASCADE, related_name="cover_images", blank=True, null=True)
    uid = models.CharField(max_length=20, blank=False, unique=True)
    cover_image = models.ImageField(upload_to="images/department_media/sub_sections/cover_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSubSectionBannerImage(models.Model):
    department_sub_section = models.ForeignKey(DepartmentSubSection, on_delete=models.CASCADE, related_name="banner_images")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    banner_image = models.ImageField(upload_to="images/department_media/sub_sections/banner_images/")
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentView(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="views")
    department_section = models.ForeignKey(DepartmentSection, on_delete=models.SET_NULL, related_name="views", blank=True, null=True)
    department_sub_section = models.ForeignKey(DepartmentSubSection, on_delete=models.SET_NULL, related_name="views", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentProductSpecification(models.Model):
    department = models.OneToOneField(Department, on_delete=models.CASCADE, related_name="specification")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentProductSpecificationItem(models.Model):
    department_product_specification = models.ForeignKey(DepartmentProductSpecification, on_delete=models.CASCADE, related_name="items")
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentProductSpecificationItemOption(models.Model):
    department_product_specification_item = models.ForeignKey(DepartmentProductSpecificationItem, on_delete=models.CASCADE, related_name="options")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSectionProductSpecification(models.Model):
    department_section = models.OneToOneField(DepartmentSection, on_delete=models.CASCADE, related_name="specification")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSectionProductSpecificationItem(models.Model):
    department_section_product_specification = models.ForeignKey(DepartmentSectionProductSpecification, on_delete=models.CASCADE, related_name="items")
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSectionProductSpecificationItemOption(models.Model):
    department_section_product_specification_item = models.ForeignKey(DepartmentSectionProductSpecificationItem, on_delete=models.CASCADE, related_name="options")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSubSectionProductSpecification(models.Model):
    department_sub_section = models.OneToOneField(DepartmentSubSection, on_delete=models.CASCADE, related_name="specification")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSubSectionProductSpecificationItem(models.Model):
    department_sub_section_product_specification = models.ForeignKey(DepartmentSubSectionProductSpecification, on_delete=models.CASCADE, related_name="items")
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class DepartmentSubSectionProductSpecificationItemOption(models.Model):
    department_sub_section_product_specification_item = models.ForeignKey(DepartmentSubSectionProductSpecificationItem, on_delete=models.CASCADE, related_name="options")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)