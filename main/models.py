from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    


class CityGroups(models.Model):
    name = models.CharField(max_length=255)
    cities = models.ManyToManyField(City)

    def __str__(self):
        return self.name



class BasicUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city  = models.OneToOneField(City)
    phone_number = models.CharField(max_length=10)
    profile_img = models.ImageField(upload_to='profile_pictures/')


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)

class Post(models.Model):
    title = models.CharField(max_length=40)
    post_type = models.OneToOneField(Category)
    image = models.ImageField(upload_to='post_images/')
    phone_number =  models.CharField(max_length=30)
    more_info = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=20)
    user = models.OneToOneField(BasicUser)
    city = models.OneToOneField(City)
    views = models.PositiveBigIntegerField(default=0)
    liked = models.PositiveBigIntegerField(default=0)