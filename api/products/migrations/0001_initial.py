# Generated by Django 4.2.4 on 2023-08-19 15:31

import api.core.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendors', '0001_initial'),
        ('product_types', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('short_description', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('price', api.core.fields.PositiveFloatField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0)])),
                ('length', models.FloatField(default=0)),
                ('width', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('length_unit', models.CharField(choices=[('in', 'Inches'), ('cm', 'Centimeters'), ('ft', 'Feet'), ('m', 'Meters')], default='ft', max_length=5)),
                ('weight', models.FloatField(default=0)),
                ('weight_unit', models.CharField(choices=[('lb', 'Pounds'), ('kg', 'Kilograms'), ('oz', 'Ounces'), ('g', 'Grams')], default='oz', max_length=5)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='categories.category')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('product_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product_types.producttype')),
                ('vendor', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='vendors.vendor')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'products',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'product_images',
                'ordering': ['id'],
            },
        ),
    ]
