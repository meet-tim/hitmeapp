from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Product(models.Model):
    CATEGORY = (
        ('Furniture','Furniture'),
        ('Appliances','Appliances'),
        ('Decor','Decor'),
        ('Tools','Tools'),
        )
    owner_id = models.CharField(max_length=100)
    name =  models.CharField(max_length=100)
    location = models.name = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    category = models.CharField(max_length=100,choices=CATEGORY)
    desc = models.TextField(max_length=200)
    date_posted = models.DateField(auto_now_add=True)
    contact =  models.PositiveIntegerField(validators=[RegexValidator(regex='^.{9}$', message='Length has to be 10', code='nomatch')])
    image = models.ImageField(upload_to='images/', )

    class Meta:
        ordering=['-date_posted',]

    def __str__(self):
        return self.name

class Best_Deals(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,primary_key=True)

class Tags(models.Model):
    name = models.CharField(max_length=100)

class Sponsored(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,primary_key=True)

class Suggestion(models.Model):
    message = models.TextField(max_length=300)
    timestamp = models.DateField(auto_now=True)
