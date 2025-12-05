
from order.models import Cart,CartItem,Order,OrderItem
from django.db import transaction
from rest_framework.exceptions import PermissionDenied,ValidationError

class OrderService:
    @staticmethod
    def create_order(user_id,cart_id):
        with transaction.atomic(): #atomic er kaj hlo jode all process complete hoi taholle success hbe or error dakhabe 
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('product').all()
            total_price = sum([item.product.price * item.quantity for item in cart_items])
            order=Order.objects.create(user_id=user_id,total_price=total_price)

            order_item =[
                OrderItem(
                    order=order,
                    product=item.product,
                    price=item.price,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_item)
            cart.delete()
            return order
    @staticmethod
    def cancel_order(order,user):
        if user.is_staff:
            order.status = Order.CANCELED
            order.save()
            return Order
        if order.user != user:
            raise PermissionDenied({'detail':'you can only cancel your own order'})

        if order.status == Order.DELEVIRED:
            raise ValidationError({'detail':'you can not cancel an order'})
        order.status = Order.CANCELED
        order.save()  
        return order
