from django.shortcuts import get_object_or_404
from django.http import HttpResponse 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from product.models import Product,Category,Review,ProductImage
from rest_framework import status 
from product.serializers import ProductSerializer,CategorySerializer,ReviewSerializer,ProductImageSerializer
from django.db.models import Count 
from rest_framework.views import APIView 
from rest_framework.mixins import CreateModelMixin,ListModelMixin 
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from  rest_framework.filters import SearchFilter,OrderingFilter
from product.filters import ProductFilter
from rest_framework.permissions import IsAdminUser,AllowAny
from api.permissions import IsAdminReadOnly
from rest_framework.permissions import DjangoModelPermissions
from product.permissions import IsReviewAuthorORReadonly
from product.paginations import DefaultPagination
from drf_yasg.utils import swagger_auto_schema


# Create your views here.          
class ProductViewSet(ModelViewSet):

    """Api endpoint for managing products in the e-commerce store
     - Allows authenticed admin to create , update and delete products
     - allows users to browes and filter product
     - support serach by name ,description and category
     - support ordering by price and updated_at
    """
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[AllowAny]

    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['name','description','category__name']
    ordering_fields=['price','updated_at']
    pagination_class=DefaultPagination

    @swagger_auto_schema(
        operation_summary='Retrive all list of product',
       
    )
    def list(self, request, *args, **kwargs):
        '''Retrive all the product'''
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Create a product by admin",
        operation_description="This allow to create a product",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: 'Bad request'
        }


    )
    def create(self, request, *args, **kwargs):
        '''Only authenticted admin can cretae product'''
        return super().create(request, *args, **kwargs)

class ProductImageViewSet(ModelViewSet):
    serializer_class=ProductImageSerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def perform_create(self,serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))

 


        
'''USING classed basaed WITH SPECFICE VIEW PRODUCTS'''
class ViewSpecficeProductMixin(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    

    def delete(self,request,pk):
        product= get_object_or_404(Product,pk=pk)
        if product.stock>10:
            return Response({'message':"Product with stock more than if could nopt bne deleted"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





'''------------------------------------------------------------'''

'''USING api view WITH VIEW CATEGORIES'''
@api_view()
def view_categories(request):
    categories=Category.objects.annotate(product_count=Count('products')).all()
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)

'''USING classed basaed WITH VIEW CATEGORIES'''
'''CLASS BASED VIEW'''


class ViewCategories(APIView):
    def get(self,requets):
        categories=Category.objects.annotate(product_count=Count('products')).all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data)
    def post(self,request):
        if request.method=='POST':
            serializer=CategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    def put(self,request,pk):
        category=get_object_or_404(Category.objects.annotate(produict_count=Count('products')).all(),pk=pk)
        serializer=CategorySerializer(category,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)        

'''USING mixin WITH VIEW CATEGORIES''' 
class ViewCategoriesMixin(ListCreateAPIView):
    queryset=Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.annotate(product_name=Count('products')).all()
    serializer_class=CategorySerializer
'''------------------------------------------------------------'''


'''------------------------------------------------------------'''
@api_view()
def view_specfice_categories(request,pk):
    category=get_object_or_404(Category,pk=pk)
    serializer=CategorySerializer(category)
    return Response(serializer.data)

'''CLASS BASED VIEW'''

class ViewSpecficCategories(APIView):
    def get(self,request,pk):
        category=get_object_or_404(Category,pk=pk)
        serializer=CategorySerializer(category)
        return Response(serializer.data)
    def put(self,request,pk):
        category=get_object_or_404(Category.objects.annotate(produict_count=Count('products')).all(),pk=pk)
        serializer=CategorySerializer(category,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)        
    def delete(self,request,pk):
        if request.method =='DELETE':
            category=get_object_or_404(Category.objects.annotate(product_count=Count('products')),pk=pk)
            category.delete
            return Response(status=status.HTTP_204_NO_CONTENT)

class ViewSpecficeCategoriesMixin(RetrieveUpdateDestroyAPIView):
    queryset=Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer
        

'''------------------------------------------------------------'''



class ReviewViewSet(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsReviewAuthorORReadonly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))


    def get_serializer_context(self):
        # Swagger safe
        return {'product_id': self.kwargs.get('product_pk')}