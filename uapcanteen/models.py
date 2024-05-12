from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Owner(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Breakfast(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    discount = models.IntegerField()
    rating = models.FloatField()
    

    def __str__(self):
        return self.name   

class Lunch(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    discount = models.IntegerField()
    rating = models.FloatField()
    SPICY_LEVEL_CHOICES = [
    ('Mild', 'Mild'),
    ('Medium', 'Medium'),
    ('Spicy', 'Spicy'),
    ('Extra Spicy', 'Extra Spicy')
    ]
    spiciness_level = models.CharField(max_length=15, choices=SPICY_LEVEL_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

class Dinner(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    discount = models.IntegerField()
    chefs_special = models.BooleanField()
    rating = models.FloatField()
    SPICY_LEVEL_CHOICES = [
    ('Mild', 'Mild'),
    ('Medium', 'Medium'),
    ('Spicy', 'Spicy')
    ]
    spiciness_level = models.CharField(max_length=15, choices=SPICY_LEVEL_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name         
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breakfast = models.ForeignKey(Breakfast, on_delete=models.CASCADE, blank=True, null=True)
    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE, blank=True, null=True)
    dinner = models.ForeignKey(Dinner, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    breakfast = models.ForeignKey(Breakfast, on_delete=models.CASCADE, blank=True, null=True)
    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE, blank=True, null=True)
    dinner = models.ForeignKey(Dinner, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order of {self.user.username}"
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name    