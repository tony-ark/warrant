from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    img = models.TextField()
    warranty = models.IntegerField()

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class Claim(models.Model):
    claim_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)