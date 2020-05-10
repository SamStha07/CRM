from django.db import models


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    # SET_NULL = if we remove the customer, there will be no value of customer in database
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name