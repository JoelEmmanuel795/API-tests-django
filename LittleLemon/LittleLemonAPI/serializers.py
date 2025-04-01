from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal
import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory', 'category']

class MenuItemSerializerLess(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title']

# Rename 'inventory' field to 'stock'
class MenuItemSerializerTaxed(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory') # Assuming 'inventory' is the field name in the model
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2) # Assuming price is a positive value higher than 2
    
    # def validate_price(self, value):
    #         if value < 2:
    #             raise serializers.ValidationError('Price should not be less than 2.0')
    #         return value  # Return value if it passes validation
        
    # def validate_stock(self, value):
    #         if value < 0:
    #             raise serializers.ValidationError('Stock cannot be negative')
    #         return value  # Return value if it passes validation
    
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if attrs['price'] < 2:
            raise serializers.ValidationError('Price should not be less than 2.0')
        if attrs['inventory'] < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)

    # def validate_title(self, value):
    #     # Clean the input to prevent XSS attacks
    #     return bleach.clean(value)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        # extra_kwargs = {
        #     'price': {'min_value': 2},  
        #     'stock':{'source':'inventory', 'min_value': 0}
        # } # Assuming price is a positive value higher than 2 and stock is a non-negative value

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)  # Assuming a tax rate of 10%