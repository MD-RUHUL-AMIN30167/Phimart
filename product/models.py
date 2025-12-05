from django.db import models
from  django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
from product.validators import validate_file_size
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null =True)
    def __str__(self):
        return self.name                 

class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to="products/images",validators= [validate_file_size])
    # file=models.FileField(upload_to='product/files',validators=FileExtensionValidator(['pdf']))


class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    # name=models.CharField(max_length=250)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ratings= models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"review by {self.user.first_name} on {self.product.name}"


'''STEP TO BUILD AN API '''
# first step ready do the model
# second step ready do the serializer
# third step ready do the ViewSet
# fourth step ready do the router
