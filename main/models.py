from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CityGroups(models.Model):
    name = models.CharField(max_length=255)
    cities = models.ManyToManyField(City)

    def __str__(self):
        return self.name


class BasicUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=90)
    profile_img = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )


class Category(models.Model):
    icon = models.FileField(upload_to="svg_icon/", blank=True, null=True)
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=40)
    post_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images/")
    phone_number = models.CharField(max_length=30)
    more_info = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=20)
    user = models.ForeignKey(BasicUser, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    views = models.ManyToManyField(
        BasicUser, related_name="views", blank=True, null=True
    )
    liked = models.ManyToManyField(
        BasicUser, related_name="liked", blank=True, null=True
    )

    def increase_views(self, user):
        self.views.add(user)
        self.save()

    def increase_likes(self, user):
        self.liked.add(user)
        self.save()

    def has_user_viewed(self, user):
        return self.views.filter(id=user.id).exists()

    def has_user_liked(self, user):
        return self.liked.filter(id=user.id).exists()
