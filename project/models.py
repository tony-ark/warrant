from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    info = models.TextField()
    warranty = models.IntegerField()

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

class Claim(models.Model):
    claim_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
    order_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)