# Generated by Django 4.2.2 on 2023-06-21 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0005_remove_merchantplan_merchant_plan_listings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantplanprice',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]