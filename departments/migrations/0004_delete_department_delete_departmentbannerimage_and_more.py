# Generated by Django 4.2.2 on 2023-06-18 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_department_and_more'),
        ('departments', '0003_remove_departmentbannerimage_department_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='DepartmentBannerImage',
        ),
        migrations.DeleteModel(
            name='DepartmentCoverImage',
        ),
        migrations.DeleteModel(
            name='DepartmentProductSpecification',
        ),
        migrations.DeleteModel(
            name='DepartmentProductSpecificationItem',
        ),
        migrations.DeleteModel(
            name='DepartmentProductSpecificationItemOption',
        ),
        migrations.DeleteModel(
            name='DepartmentSection',
        ),
        migrations.DeleteModel(
            name='DepartmentSectionBannerImage',
        ),
        migrations.DeleteModel(
            name='DepartmentSectionCoverImage',
        ),
        migrations.DeleteModel(
            name='DepartmentSectionProductSpecification',
        ),
        migrations.DeleteModel(
            name='DepartmentSectionProductSpecificationItem',
        ),
        migrations.DeleteModel(
            name='DepartmentSectionProductSpecificationItemOption',
        ),
        migrations.DeleteModel(
            name='DepartmentSubSection',
        ),
        migrations.DeleteModel(
            name='DepartmentSubSectionBannerImage',
        ),
        migrations.DeleteModel(
            name='DepartmentSubSectionCoverImage',
        ),
        migrations.DeleteModel(
            name='DepartmentSubSectionProductSpecification',
        ),
        migrations.DeleteModel(
            name='DepartmentSubSectionProductSpecificationItem',
        ),
        migrations.DeleteModel(
            name='DepartmentSubSectionProductSpecificationItemOption',
        ),
        migrations.DeleteModel(
            name='DepartmentView',
        ),
    ]
