from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Gadget(models.Model):
    product_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    warranty = models.DateTimeField()