from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User


# Create your models here.
class CustomeManager(models.Manager):
    def get_price_range(self, r1, r2):
        return self.filter(price__range=(r1, r2))

    def doglist(self):
        return self.filter(category__exact="Dog")

    def catlist(self):
        return self.filter(category__exact="Cat")

    def Collars(self):
        return self.filter(category__exact="Collars")

    def Toys(self):
        return self.filter(category__exact="Toys")
    
    def Foods(self):
        return self.filter(category__exact="Foods")
    
    def Grooming(self):
        return self.filter(category__exact="Grooming")
    
    def Clothing(self):
        return self.filter(category__exact="Clothing")
    
    def Health(self):
        return self.filter(category__exact="Health")
    
    def Housing(self):
        return self.filter(category__exact="Housing")
    
class Pet(models.Model):
    pet_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    type = (("Cat", "Cat"), ("Dog", "Dog"), ("Collars", "Collars"),("Toys", "Toys"),("Foods", "Foods"),("Grooming", "Foods"),("Clothing", "Clothing"),("Housing", "Housing"), ("Health", "Health"))
    category = models.CharField(max_length=100, choices=type)
    desc = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="pics")

    pet = CustomeManager()  # customer manager
    objects = models.Manager()  # default manager

    @property
    def proImage(self):
        return mark_safe(f"<img src='{self.image.url}' width='300px'>")
    
class CartItem(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)



class Order(models.Model):
    order_id = models.CharField(max_length=50)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    payment_screenshot = models.ImageField(upload_to='proof', null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
    
    
    
    
from django.db import models



class GroomingReservation(models.Model):
    PET_TYPE_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null and blank for now
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=50, choices=PET_TYPE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default='00:00:00')
    
    def __str__(self):
        return f"{self.pet_name} ({self.pet_type}) - {self.appointment_date} at {self.appointment_time}"