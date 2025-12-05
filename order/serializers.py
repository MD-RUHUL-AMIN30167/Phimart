from rest_framework import serializers
from order.models import Cart,CartItem,Order,OrderItem
from product.serializers import ProductSerializer
from product.models import Product
from order.services import OrderService

class EmpltySerializer(serializers.Serializer):
    pass

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['id','name','price']


# class AddCartItemSerializer(serializers.ModelSerializer):
#     product_id=serializers.IntegerField()
#     class Meta:
#         model = CartItem
#         fields = ['id','product_id','quantity']
#     def save(self,**kwargs):
#         cart_id=self.context['cart_id']
#         product_id=self.validated_data['product_id']
#         quantity=self.validated_data['quantity']
#         # cart = Cart.objects.get(id=cart_id)
#         # product = Product.objects.get(id=product_id)
#         try:
#             cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
#             cart_item.quantity += quantity
#             self.instance = cart_item.save()
            
#         except CartItem.DoesNotExist:
#             self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data)

#         return self.instance  


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            raise serializers.ValidationError({"cart": "Cart does not exist."})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product": "Product does not exist."})

        
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()  
            self.instance = cart_item  
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    # product_price=serializers.SerializerMethodField(method_name='get_product_price')
    class Meta:
        model=CartItem
        fields=['id','product','quantity','product','total_price']
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price

    #how do you related fileld add 
    # def get_product_price(self,cart):
    #     return cart.product.price


class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model=Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields=['user']

    def get_total_price(self, cart: Cart):
        return sum(
            [item.product.price * item.quantity for item in cart.items.all()])
   

class CreateOrderSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No Cart Found eith is id')
        
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')
        return cart_id
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']
        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))


    def to_representation(self, instance):
        return OrderSerializer(instance).data

class OrderItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields=['id' ,'product','quantity','price','total_price']
   
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields=['status']


    # def updated(self,instance,validated_data):
        # user=self.context['user']
        # new_status = validated_data['status']
        # if new_status == Order.CANCELED:
        #     return OrderService.cancel_order(order=instance,user=user)
        # #admin kina 
        # if not user.is_staff:
        #     raise serializers.ValidationError({'detail':'you are not allowed update this order'})
        
        # return super().update(instance,validated_data)


class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields=['id','user','status','total_price','created_at','items']


