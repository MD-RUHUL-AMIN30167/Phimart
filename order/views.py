from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from order.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,OrderSerializer,OrderItemSerializer,CreateOrderSerializer,UpdateOrderSerializer,EmpltySerializer
from order.models import Cart,CartItem,Order,OrderItem
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response

# Create your views here.


class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    # queryset=Cart.objects.all()
    serializer_class=CartSerializer
    # permission_classes=[BasePermission]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)
    
class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        if getattr(self,'swagger_fake_view',False):
            return{}
        return {'cart_id':self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs.get('cart_pk'))

class OrderViewSet(ModelViewSet):
    # queryset=Order.objects.all()
    # serializer_class=OrderSerializer
    
    http_method_names=['get','post','delete','patch','head','options']
    # permission_classes=[IsAuthenticated]
    @action(detail=True,methods=['post'])
    def cancel(self,request,pk=None):
        order=self.get_objects()
        OrderService.cancel_order(order=order,user=request.user)
        return Response({'status':'Your order cancled'})
    @action(detail=True,methods=['patch'])
    def update_status(self,request,pk=None):
        order=self.get_object()
        serializer = UpdateOrderSerializer(order,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": f"order update successfully {request.data['status']}"})




    def get_permissions(self):
        if self.action in ['update_status','destory']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
        
    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmpltySerializer
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'update_status':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        # Swagger safe
        if getattr(self, 'swagger_fake_view', False) or self.request.user.is_anonymous:
            return {}
        return {'user_id': self.request.user.id, 'user': self.request.user}

        
    
    # def get_queryset(self):
    #     if self.request.user.is_staff:
    #         return Order.objects.prefetch_related('items__product').all()
    #     return Order.objects.prefetch_related('items__product').filter(user=self.request.user)
    def get_queryset(self):
        # Swagger safe
        if getattr(self, 'swagger_fake_view', False) or self.request.user.is_anonymous:
            return Order.objects.none()

        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()

        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)


class OrderItemViewSet(ModelViewSet):
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    permission_classes=[]
