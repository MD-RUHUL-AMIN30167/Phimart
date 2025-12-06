from rest_framework import serializers
from decimal import Decimal
from product.models import Category,Product,Review,ProductImage
# from django.conf import settings
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):

    product_count=serializers.SerializerMethodField()
    class Meta:
        model=Category
        fields=['id','name','description','product_count']
    def get_product_count(self,obj):
        return obj.products.count()
        

        
# class ProductSerializer(serializers.Serializer):
#     id=serializers.IntegerField()
#     name=serializers.CharField()
#     unit_price=serializers.DecimalField(max_digits=10,decimal_places=2,source ='price')
#     price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
#     #category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     #category=CategorySerializer()
#     category=serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(),
#         view_name='view_specfic_categories',       
#     )
#     def calculate_tax(self,product):
#         return product.price * Decimal(1.1)
#product er image 
class ProductImageSerializer(serializers.ModelSerializer):
    image=serializers.ImageField()
    class Meta:
        model=ProductImage
        fields=['id','image']

class ProductSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True)
    class Meta:
        model=Product
        fields=['id','name','description','price','stock','images','category','created_at','updated_at','price_with_tax']
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')  
    category=serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        # view_name='view_specfic_categories',
        view_name='category-detail',
    )  
    # category=CategorySerializer()
    def calculate_tax(self,product):
        return product.price * Decimal(1.1)




class SimpleUserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model=get_user_model()
        fields=['id','name']
    def get_current_user_name(self,obj):
        return obj.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    # user=SimpleUserSerializer()
    # product=serializers.CharField(read_only=True)
    user=serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model=Review
        fields=['id','user','product','ratings','comment']
    
    def get_user(self,obj):
        return SimpleUserSerializer(obj.user).data
    
    def create(self,validated_data):
        product_id=self.context['product_id']
        review=Review.objects.create(product_id=product_id,**validated_data)
        return review