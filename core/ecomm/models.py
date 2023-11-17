from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

SIZE = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)

CATEGORIES = (
    ('SH','Shirt'),
    ('TS','T-Shirt'),
    ('TR','Trouser'),
)

class Product(models.Model):
    title = models.CharField(max_length=120)
    desc = models.CharField(max_length=500)
    price = models.FloatField(default=0.00)
    size = models.CharField(choices=SIZE, max_length=2)
    category = models.CharField(choices=CATEGORIES, max_length=2)
    img1 = models.ImageField(upload_to='ecomm/images', default='')
    img2 = models.ImageField(upload_to='ecomm/images', default='')
    img3 = models.ImageField(upload_to='ecomm/images', default='')

    def __str__(self):
        return self.title

    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_by_category(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    card_name = models.CharField(max_length=200, blank=True)
    card_number = models.CharField(max_length=20, blank=True)
    card_cvv = models.IntegerField(default=0)

    def placeOrder(self):
        self.save()
