# Generated by Django 4.0.4 on 2023-06-07 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='products.product'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_variant_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='products.productvariantitem'),
        ),
    ]
