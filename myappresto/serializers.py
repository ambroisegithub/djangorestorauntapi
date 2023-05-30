from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields =['id','slug','title']
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source="invertory")
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = CategorySerializer()

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.create(**category_data)
        validated_data['category'] = category
        return MenuItem.objects.create(**validated_data)

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
        
#class to handle class MenuItem1 from models.py 
class MenuItemSerializer1(serializers.Serializer):
    
    id = serializers.IntegerField()
    Title = serializers.CharField(max_length=255)
    Price = serializers.DecimalField(max_digits=6,decimal_places=2)
    Invertory = serializers.CharField()
    
