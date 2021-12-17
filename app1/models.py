from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Users(models.Model):
    name=models.CharField(max_length=144)
    lastname=models.CharField(max_length=144)
    email=models.EmailField()
    password=models.CharField(max_length=150)
    default_shipping_address=models.CharField(max_length=150)
    country=models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"id: {self.id}, Name:{self.name}, email:{self.lastname}"

class Product(models.Model):
    nombre=models.CharField(max_length=144)
    price=models.FloatField()
    description=models.TextField()
    # el parametro "upload_to" creará una subcarpeta dentro de "media" para guardar las imagenes
    # el null=True es si no tenemos una imgen
    image=models.ImageField(upload_to="productos", null=True)

    # PositiveInteger OPC ->
    stock=models.IntegerField(validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Categorias(models.Model):
    # Ropa para niños, para adultos, tecnologías
    name_category=models.CharField(max_length=144)
    description_category=models.TextField()
    # Revisar ( )
    key_catogory_list=models.ManyToManyField(Product)

class Orders(models.Model):
    user_id=models.ForeignKey(Users, on_delete=models.CASCADE)
    shipping_address=models.TextField()
    order_address=models.TextField()
    order_email=models.TextField()
    order_date=models.TextField()
    order_status=models.TextField()
    # ammount=models.ManyToManyField()

class Order_details(models.Model):
    order_id=models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.FloatField()
    quantity=models.PositiveIntegerField()


